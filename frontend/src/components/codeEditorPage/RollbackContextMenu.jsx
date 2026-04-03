import styles from "../../css/CodeEditor.module.css";
import {Fragment, useEffect, useState} from "react";
import {HTTPMethods, httpRequest, printError} from "../../utils/requests.js";
import {useParams} from "react-router";

export const RollbackContextMenu = ({setGlobalContextMenu}) => {

  const {id} = useParams()
  const [isProcessing, setIsProcessing] = useState(false)

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest(`.${styles.globalContextMenu}`)) {
        setGlobalContextMenu(null)
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [setGlobalContextMenu]);

  const rollback = (e, hard) => {
    e.stopPropagation()
      httpRequest(HTTPMethods.DELETE, "/api/events/project/rollback", {projectId: id, hard: hard},
          {}, true)
          .then(() => {
            if (hard)
              location.reload()
            else
              setGlobalContextMenu(null)
          }).catch(printError)
  }

  if (isProcessing)
    return (<div className={"cloudyBackground"}>
        <div className={styles.globalContextMenu}>
          <span className={"loader"}></span>
        </div>
    </div>)

  return (
      <div className={"cloudyBackground"}>
        <div className={styles.globalContextMenu}>
          <div className={styles.rollbackButtons}>
            <button type={"submit"} onClick={(e) => rollback(e, false)}>Мягкий откат</button>
            <button type={"submit"} onClick={(e) => rollback(e,true)}>Жесткий откат</button>
          </div>
        </div>
      </div>
  )
}