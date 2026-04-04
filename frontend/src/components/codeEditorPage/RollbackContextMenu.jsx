import styles from "../../css/CodeEditor.module.css";
import {Fragment, useEffect, useRef, useState} from "react";
import {HTTPMethods, httpRequest, printError} from "../../utils/requests.js";
import {useParams} from "react-router";


const isHardRollback = (hard, setGlobalContextMenu) => {
    if (hard)
      location.reload()
    else
      setGlobalContextMenu(null)
}

export const RollbackContextMenu = ({setGlobalContextMenu}) => {

  const {id} = useParams()
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState(null)
  const [conflictHandlers, setConflictHandlers] = useState([])
  const [hardRollback, setHardRollback] = useState(false)

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest(`.${styles.globalContextMenu}`)) {
        setGlobalContextMenu(null)
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [setGlobalContextMenu]);

  const tryToRollback = (e, hard) => {
    e.stopPropagation()
    setIsProcessing(true)
    setHardRollback(hard)

    httpRequest(HTTPMethods.DELETE, "/api/events/project/rollback", {projectId: id, hard: hard},
        {}, true)
        .then(() => isHardRollback(hard, setGlobalContextMenu))
        .catch((err) => {
          const details = err.response.data?.detail
          setIsProcessing(false)

          if (details?.type === "conflict handlers") {
            setError("Данные функции не были созданы до текущей версии проекта. Они будут удалены!")
            setConflictHandlers(details.details)
          } else if (details?.type === "v0")
            setError("Откат невозможен. Данная версия проекта является первой.")
        })
  }

  if (isProcessing)
    return (
      <div className={"cloudyBackground"}>
        <span className={"loader dark"}></span>
      </div>)

  return (
      <div className={"cloudyBackground"}>
        <div className={styles.globalContextMenu}>
          <div className={styles.rollbackButtons}>
            {error ? <RollbackErrorState error={error}
                                         handlers={conflictHandlers}
                                         setGlobalContextMenu={setGlobalContextMenu}
                                         setIsProcessing={setIsProcessing}
                                         hard={hardRollback}/>
              : (
              <>
                <button type={"submit"} onClick={(e) => tryToRollback(e, false)}>Мягкий откат</button>
                <button type={"submit"} onClick={(e) => tryToRollback(e,true)}>Жесткий откат</button>
              </>
            )}

          </div>
        </div>
      </div>
  )
}

const RollbackErrorState = ({error, handlers, setGlobalContextMenu, setIsProcessing, hard}) => {

  const {id} = useParams()

  const continueRollback = (e) => {
    e.stopPropagation()
    setIsProcessing(true)

    let deleteCount = 0
    for (let handler of handlers) {
      const service = handler.service
      httpRequest(HTTPMethods.DELETE, "/api/events/functions/delete-" + service, {functionId: handler.id},
          {}, true)
          .then(() => {
            deleteCount++
            if (deleteCount === handlers.length)
              httpRequest(HTTPMethods.DELETE, "/api/events/project/rollback", {projectId: id, hard: hard},
                  {}, true)
                  .then(() => isHardRollback(hard, setGlobalContextMenu))
          })
    }
  }

  return (
       <div className={styles.error}>
         <div style={{textAlign: "center"}}>
           <h3>{error}</h3>
         </div>
         <div className={styles.conflictHandlers}>
           {handlers.map(e => <div key={e.handlerPath}><b>{e.name}</b> - {e.handlerPath}:{e.handler}</div>)}
         </div>
         {handlers.length > 0 && (
           <div className={styles.continueConflictHandlersButton}>
             <button onClick={e => continueRollback(e, false)}>Продолжить</button>
           </div>
         )}

       </div>
   )
}