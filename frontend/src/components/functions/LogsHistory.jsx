import styles from "../../css/Function.module.css"
import {useEffect, useState} from "react";
import BTree from "sorted-btree";
import {getStringDate} from "../../utils/formats.js";
import {data, useNavigate} from "react-router";

export const LogsHistory = () => {
  const [logsHistory, setLogsHistory] = useState(new BTree(undefined, () => {}))
  const navigate= useNavigate()

  useEffect(() => {
    const data = Array.from({ length: 10 }, (_, i) => ({
      runId: Math.random().toString(16).substring(2, 32), // Уникальный ID
      lastStart: Date.now() - i * 1000,
      totalTime: "0.025 мс",
      isActive: false
    }));

    const tree = new BTree(undefined, (a, b) => {
      const timeDiff = b.lastStart - a.lastStart;
      if (timeDiff !== 0) return timeDiff;

      if (a.runId === b.runId) return 0;
      return a.runId > b.runId ? 1 : -1;
    });
    data.forEach(log => {
      tree.set(log, true)
    })

    setLogsHistory(tree)
  }, []);

  const openLogs = (data) => {
    navigate(`logs/${data.runId}`, {
      state: {
        runData: data
      }
    })
  }

  return (
      <div className={styles.logsBox}>
        <h3>История выполнений</h3>
        {logsHistory.keysArray().map(e => {
          return (
            <div className={styles.logElement} onClick={() => openLogs(e)}>
              <div className={styles.id}>{e.runId}</div>
              <div className={styles.info}>Последний запуск: {getStringDate(e.lastStart)}</div>
              {
                e.isActive ? (
                  <div className={styles.isActive}>
                    <div className={styles.activeCircle}></div>
                    Выполняется
                  </div>
                ) :
                (
                    <div className={styles.info}>Время выполнения: {e.totalTime}</div>
                )
              }
          </div>
          )
        })}
         </div>
  )
}