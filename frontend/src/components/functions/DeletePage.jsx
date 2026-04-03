import styles from "../../css/Function.module.css"
import {useEffect, useState} from "react";
import {HTTPMethods, httpRequest, printError} from "../../utils/requests.js";
import {useNavigate, useParams} from "react-router";

export const DeletePage = () => {

  const {id} = useParams()
  const [service, setService] = useState(null)
  const navigate = useNavigate()

   const handlerDelete = () => {
     httpRequest(HTTPMethods.DELETE, "/api/events/functions/delete-" + service,
         {functionId: id}, {}, true)
         .then(() => navigate("../..", { relative: 'path' })).catch(printError)
  }

  useEffect(() => {
    const stateService = location?.state?.service
    if (stateService) {
      setService(stateService)
    } else {
      httpRequest(HTTPMethods.GET, "/api/events/functions/get", {functionId: id})
        .then((e) => {
          setService(e.data.service)
        })
    }
  }, [])

  if (!service)
    return (<div className={styles.modalContent}><span className={"loader dark"}></span></div>)

  return (
    <div className={styles.modalContent}>
      <div className={styles.formWindow + " " + styles.center}>
        <div style={{fontSize: "20px"}}>Вы уверены, что хотите удалить функцию?</div>
        <button id={styles.deleteFunctionButton} onClick={handlerDelete}>Удалить</button>
      </div>
    </div>
  )
}