import styles from "../../css/Function.module.css"
import {useEffect, useState} from "react";
import BTree from "sorted-btree";
import {getStringDate} from "../../utils/formats.js";
import {data, useNavigate} from "react-router";
import {HTTPMethods, httpRequest} from "../../utils/requests.js";

export const LogsHistory = ({id}) => {
  const [logsHistory, setLogsHistory] = useState(null)
  const navigate= useNavigate()

  useEffect(() => {
    const tree = new BTree(undefined, (a, b) => {
      const timeDiff = b["createdAt"] - a["createdAt"]
      if (timeDiff !== 0) return timeDiff

      if (a["id"] === b["id"]) return 0
      return a["id"] > b["id"] ? 1 : -1
    });

    httpRequest(HTTPMethods.GET, "/api/events/execution_logs/get-all", {functionId: id})
        .then((e) => {
          const logs = e.data.map((e) => ({...e, isActive: false}))
          logs.forEach(log => {
            tree.set(log, true)
          })
          setLogsHistory(tree)
        })

  }, []);

  const openLogs = (logData) => {
    navigate(`logs/` + logData.id, {
      state: {
        logData: logData
      }
    })
  }

  return (
      <div className={styles.logsBox}>
        <h3>История выполнений</h3>
        {!logsHistory ? <div className={styles.logsBox}><span className={"loader dark"}></span></div> :
          Array.from(logsHistory.keys()).map(e => {
            return (
              <div className={styles.logElement} onClick={() => openLogs(e)}>
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
                      <div className={styles.info}>Время выполнения: {e.executionTime} мс</div>
                  )
                }
            </div>
            )
          })}
         </div>
  )
}