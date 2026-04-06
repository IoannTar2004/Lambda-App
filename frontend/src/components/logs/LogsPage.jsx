import styles from "../../css/Logs.module.css"
import {useLocation, useParams} from "react-router";
import {useEffect, useRef, useState} from "react";
import {HTTPMethods, httpRequest} from "../../utils/requests.js";
import {getStringDateLog} from "../../utils/formats.js";
import {RingBuffer} from "../../utils/ringBuffer.js";

export const LogsPage = () => {

  const {id, run_id} = useParams()
  const location = useLocation()
  const [logData, setLogData] = useState(null)

  const logRef = useRef(null)
  const isLogsLoaded= useRef(false)
  const isStreaming = useRef(false)
  const ws = useRef(null)
  const logBuffer = useRef(new RingBuffer(1000))

  const decodeUnicodeEscapes = (str) => {
    if (!str || typeof str !== 'string') return str

    return str.replace(/\\u([0-9a-fA-F]{4})/g, (_, hex) => {
        return String.fromCharCode(parseInt(hex, 16))
    })
}

  const parseAndPrintLogs = (row) => {
    if (!logRef.current) return

    const timestamp = row.timestamp
    const unixTime = parseInt(timestamp.split("-")[0])
    const text = decodeUnicodeEscapes(row.text)

    const newLog = `[${getStringDateLog(unixTime)}] ${text}\n`

    const currentContent = logRef.current.textContent
    if (currentContent.endsWith(newLog)) {
      return
    }

    logRef.current.textContent += newLog

  }

  const flushBuffer = () => {
    let log
    while (true) {
      log = logBuffer.current.dequeue()
      if (!log)
        break

      parseAndPrintLogs(log)
    }
  }

  const webSocketOnMessage = (event, ws) => {
    const msg = JSON.parse(event.data)
    if (msg.id !== run_id)
      return

    if (!isLogsLoaded.current) {
      httpRequest(HTTPMethods.GET, "/api/execution/log/get-logs-part", {runId: run_id, end: msg.timestamp})
          .then(e => {
            const firstLogs = e.data
            firstLogs.map(l => {
              const log = {timestamp: l.timestamp, text: l.text.text}
              parseAndPrintLogs(log)
            })
            isStreaming.current = true
          })
      isLogsLoaded.current = true
    }

    else if (true) {
      if (msg.type === "log") {
        logBuffer.current.enqueue(msg)

        if (isStreaming.current) {
          const log = logBuffer.current.dequeue()
          parseAndPrintLogs(log)
        }
      } else if (msg.type === "stop") {
        flushBuffer()
        ws.close()
      }
    }
  }



  useEffect(() => {
    let token = localStorage.getItem("accessToken")
    token = token.substring(7)

    httpRequest(HTTPMethods.GET, "/api/execution/log/is-active-function", {runId: run_id})
        .then(() => {
          ws.current = new WebSocket("ws://localhost:8003/api/execution/log/ws?token=" + token)

          ws.current.onmessage = (event) => {
            webSocketOnMessage(event, ws)
          }
        })
        .catch(() => {
          httpRequest(HTTPMethods.GET, "/api/code/user-files/download-log", {
            functionId: id,
            log_id: run_id
          }).then(e => {
            if (!isLogsLoaded.current) {
              e.data.map(parseAndPrintLogs)
              isLogsLoaded.current = true
            }
          })
        })

    if (ws.current?.readyState === WebSocket.OPEN || ws.current?.readyState === WebSocket.CONNECTING)
      return () => ws.current.close()
  }, [])

  return (
      <div className={styles.content}>
        <h1>{run_id}</h1>
        <pre ref={logRef} className={styles.logsField} id={"logsPage-area"}>
          {!logData && <span className={"loader"}></span>}
        </pre>
      </div>
  )
}