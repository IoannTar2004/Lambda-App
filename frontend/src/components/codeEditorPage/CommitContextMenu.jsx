import styles from "../../css/CodeEditor.module.css"
import {Fragment, useEffect, useRef, useState} from "react";
import {HTTPMethods, httpRequest, printError} from "../../utils/requests.js";
import {useParams} from "react-router";

export const CommitContextMenu = ({globalContextMenu, setGlobalContextMenu}) => {

  const {id} = useParams()
  const [deletedFiles, setDeletedFiles] = useState(null)
  const [handlers, setHandlers] = useState([])

  const commit = (e) => {
    e.stopPropagation()

    if (!deletedFiles) return

    const data =  {
      projectId: id,
      functions: {}
    }
    for (let handler of handlers) {
      const find = deletedFiles.filter(e => e.id === handler.id)[0]
      if (find.handlerPath !== handler.handlerPath && handler.handlerPath !== "")
        data.functions[handler.id] = {
          functionPath: handler.handlerPath,
          functionName: handler.handler
        }
    }

    setDeletedFiles(null)
    httpRequest(HTTPMethods.POST, "/api/events/project/commit-project", data)
        .then(() => setGlobalContextMenu(null)).catch(() => setGlobalContextMenu(null))
  }

  const handlerInputOnChange = (e, id) => {
    const text = e.target.value
    let newHandlers = [...handlers]
    newHandlers.map(e => {
      if (e.id === id)
        e.handlerPath = text
    })
    setHandlers(newHandlers)
  }

  useEffect(() => {
    httpRequest(HTTPMethods.GET, "/api/events/functions/get-deleted-files", {projectId: id  })
        .then(e => {
          if (!globalContextMenu) return

          const files = e.data
          if (files.length > 0) {
            setDeletedFiles(files.map(file => ({ ...file })))
            setHandlers(files)
          }
          else {
            setDeletedFiles(null)
            httpRequest(HTTPMethods.POST, "/api/events/project/commit-project", {
              projectId: id,
              functions: {}
            })
                .then(() => setGlobalContextMenu(null)).catch(() => setGlobalContextMenu(null))
          }
        })
  }, []);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest(`.${styles.globalContextMenu}`)) {
        setGlobalContextMenu(null)
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [setGlobalContextMenu]);

  if (!deletedFiles)
    return (
      <div className={"cloudyBackground"}>
        <span className={"loader"}></span>
      </div>)

  return (
      <div className={"cloudyBackground"}>
        <div className={styles.globalContextMenu}>
          <header>
            <h3>
              Некоторые файлы с функциями не были найдены в проекте! Возможно они были перенесены или удалены вами. Вы
              можете вручную изменить пути до файлов с вашими функциями.
            </h3>
          </header>

          {handlers.map(e => (
            <Fragment key={e.id}>
              <label>{e.handler}</label>
              <input value={e.handlerPath} onChange={s => handlerInputOnChange(s, e.id)}/>
            </Fragment>
          ))}
          <div className={styles.submit}>
            <button type={"submit"} onClick={commit}>Деплой</button>
          </div>
        </div>
      </div>
  )
}