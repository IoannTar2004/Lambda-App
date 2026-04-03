import styles from "../../css/Function.module.css"
import {useEffect, useState} from "react";
import {HTTPMethods, httpRequest, printError} from "../../utils/requests.js";
import {useNavigate, useParams} from "react-router";

export const DeleteProjectPage = () => {

  const {projectId} = useParams()
  const navigate = useNavigate()

  const [isProcessing, setIsProcessing] = useState(false)

   const handlerDelete = () => {
    setIsProcessing(true)
     httpRequest(HTTPMethods.DELETE, "/api/events/project/delete", {projectId: projectId}, {}, true)
         .then(() => navigate("../start")).catch(printError)
  }

  if (isProcessing)
    return (<div className={styles.modalContent}><span className={"loader dark"}></span></div>)

  return (
    <div className={styles.modalContent}>
      <div className={styles.formWindow + " " + styles.center}>
        <div style={{fontSize: "20px"}}>Вы уверены, что хотите удалить проект?</div>
        <button id={styles.deleteFunctionButton} onClick={handlerDelete}>Удалить</button>
      </div>
    </div>
  )
}