import styles from "../../css/Function.module.css"
import {useLocation, useNavigate, useParams} from "react-router";
import {useEffect, useState} from "react";
import {HTTPMethods, httpRequest, printError} from "../../utils/requests.js";
export const EditPage = () => {

  const {id} = useParams()
  const location = useLocation()
  const [parameters, setParameters] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const functionDescription = location?.state?.functionDescription
    if (functionDescription) {
        setParameters(functionDescription)
    } else {
      httpRequest(HTTPMethods.GET, "/api/events/functions/get", {functionId: id})
        .then((e) => {
          setParameters(e.data)
        })
    }
  }, []);

  const handleSave = () => {
    httpRequest(HTTPMethods.PATCH, "/api/events/functions/update-handler", {
      functionId: parameters.id,
      handlerPath: parameters.handlerPath,
      handler: parameters.handler,
      memorySize: parameters.memorySize,
      timeout: parameters.timeout
    }).then(() => navigate("..", { relative: 'path' })).catch(printError)
    setParameters(null)
  }

  if (!parameters)
    return (<div className={styles.modalContent}><span className={"loader dark"}></span></div>)

  return (
      <div className={styles.modalContent}>
        <div className={styles.formWindow}>
          <div className={styles.head}>Путь к обработчику</div>
          <input value={parameters.handlerPath} onChange={(e) =>
              setParameters({...parameters, handlerPath: e.target.value})}/>

          <div className={styles.head}>Обработчик</div>
          <input value={parameters.handler} onChange={(e) =>
              setParameters({...parameters, handler: e.target.value})}/>

          <div className={styles.head}>Размер памяти</div>
          <select onChange={e =>
              setParameters({...parameters, memorySize: e.target.value})}>
            <option value={"128"}>128 МБ</option>
            <option value="256">256 МБ</option>
            <option value="512">512 МБ</option>
            <option value="1024">1024 МБ</option>
          </select>

          <div className={styles.head}>Таймаут (в секундах)</div>
          <input type={"number"} max={300} min={1} value={300} onChange={(e) =>
              setParameters({...parameters, timeout: e.target.value})}/>
          <div className={styles.saveParametersBox}>
            <button id={styles.saveParametersButton} onClick={handleSave}>Сохранить</button>
          </div>
        </div>
      </div>
  )
}
