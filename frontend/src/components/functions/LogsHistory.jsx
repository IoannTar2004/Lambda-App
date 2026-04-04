import styles from "../../css/Function.module.css"
import {useEffect, useRef, useState} from "react";
import BTree from "sorted-btree";
import {getStringDate} from "../../utils/formats.js";
import {data, useNavigate, useParams} from "react-router";
import {HTTPMethods, httpRequest} from "../../utils/requests.js";

export const LogsHistory = ({id}) => {

  const streamingLogsMap = useRef(new Map())
  const [logs, setLogs] = useState(null);
  const navigate= useNavigate()

  useEffect(() => {
    const comparator = (a, b) => {
      const timeA = new Date(a.createdAt).getTime();
      const timeB = new Date(b.createdAt).getTime();

      const timeDiff = timeB - timeA
      if (timeDiff !== 0) return timeDiff

      if (a["id"] === b["id"]) return 0
      return a["id"] > b["id"] ? 1 : -1
    }

    httpRequest(HTTPMethods.GET, "/api/events/execution_logs/get-all", {functionId: id})
        .then((e) => {
          const logs = e.data.map((e) => ({...e, isActive: false}))
          logs.sort(comparator)
          setLogs(logs)
        })

    let token = localStorage.getItem("accessToken")
    token = token.substring(7)

    const ws = new WebSocket("ws://localhost:8003/api/execution/log/ws?token=" + token)

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data)
      console.log(Number(msg["function_id"]), Number(id))
      if (msg["function_id"] !== parseInt(id)) return

      const log = {
        id: msg["id"],
        createdAt: parseFloat(msg["start_time"]) * 1000,
        executionTime: parseFloat(msg["text"]),
        isActive: msg["type"] === "log"
      }

      if (!streamingLogsMap.current.has(msg["id"])) {
        streamingLogsMap.current.set(msg["id"], true)
        setLogs(prevState => {
          prevState = [...prevState, log]
          prevState.sort(comparator)
          return prevState
        })
      } else if (msg["type"] === "stop") {
        streamingLogsMap.current.delete(msg["id"])

        setLogs(prevState => {
          prevState = prevState.filter(e => e.id !== msg["id"])
          prevState = [...prevState, log]
          prevState.sort(comparator)
          return prevState
        })

      }
    }

    return () => ws.close()
  }, []);

  const openLogs = (logData) => {
    navigate(`logs/` + logData.id, {
      state: {
        logData: logData,
      }
    })
  }

  const getExecutionTime = (time) => {
    const timeScaled = time <= 0.001 ? time * 1000 : time
    const timeUnit = time <= 0.001 ? "мс" : "с"
    const round = parseFloat(timeScaled.toFixed(5))
    return `${round} ${timeUnit}`
  }

  return (
      <div className={styles.logsBox}>
        <h3>История выполнений</h3>
        {!logs ? <div className={styles.logsBox}><span className={"loader dark"}></span></div> :
          logs.map(e => {
            return (
              <div key={e.id} className={styles.logElement} onClick={() => openLogs(e)}>
                <div className={styles.id}>{e.id}</div>
                <div className={styles.info}>Время запуска: {getStringDate(e.createdAt, true)}</div>
                {
                  e.isActive ? (
                    <div className={styles.isActive}>
                      <div className={styles.activeCircle}></div>
                      Выполняется
                    </div>
                  ) :
                  (
                      <div className={styles.info}>Время выполнения: {getExecutionTime(e.executionTime)}</div>
                  )
                }
            </div>
            )
          })}
         </div>
  )
}