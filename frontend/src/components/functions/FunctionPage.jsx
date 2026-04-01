import styles from "../../css/Function.module.css"
import {useEffect, useState} from "react";
import {useLocation, useNavigate, useParams} from "react-router";
import {FunctionDescription} from "./FunctionDescription.jsx";
import {getLanguageIconByExtension, languageExtensionIcons} from "./LanguageIcons.jsx";
import {LogsHistory} from "./LogsHistory.jsx";
import {CiEdit} from "react-icons/ci";
import {MdDeleteOutline} from "react-icons/md";
import {HTTPMethods, httpRequest} from "../../utils/requests.js";

export const FunctionPage = () => {

  const {id} = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const functionData = location?.state?.description

  const [functionDescription, setFunctionDescription] = useState(null)

  useEffect(() => {
    if (functionData)
      setFunctionDescription(functionData)

    else
      httpRequest(HTTPMethods.GET, "/api/events/functions/get", {functionId: id})
        .then((e) => {
          console.log(e.data)
          setFunctionDescription(e.data)
        })
  }, []);

  const editFunction = () => {
    navigate("edit", {
      state: {
        functionData: functionData
      }
    })
  }

  const deleteFunction = () => {
    navigate("delete", {
      state: {
        functionData: functionData
      }
    })
  }

  if (!functionDescription)
    return <div className={styles.content}><span className={"loader dark"}></span></div>

  return (
      <div className={styles.content}>
        <h2>{getLanguageIconByExtension(functionDescription.handlerPath)} {functionDescription?.name}</h2>
        <div className={styles.contentFlex}>
          <div className={styles.contentFlexLeft}>
            <FunctionDescription description={functionDescription} />
            <div className={styles.functionButtons}>
              <CiEdit title={"Редактировать"} onClick={editFunction}
                      className={styles.functionButton + " " + styles.editButton}/>
              <MdDeleteOutline title={"Удалить"} onClick={deleteFunction}
                               className={styles.functionButton + " " + styles.deleteButton}/>
            </div>
          </div>
          <LogsHistory id={id} />
        </div>

      </div>
  )
}