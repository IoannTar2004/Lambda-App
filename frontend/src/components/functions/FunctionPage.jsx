import styles from "../../css/Function.module.css"
import {useEffect} from "react";
import {useLocation, useNavigate} from "react-router";
import {FunctionDescription} from "./FunctionDescription.jsx";
import {languageIcons} from "./LanguageIcons.jsx";
import {LogsHistory} from "./LogsHistory.jsx";
import {CiEdit} from "react-icons/ci";
import {MdDeleteOutline} from "react-icons/md";

export const FunctionPage = () => {

  const navigate = useNavigate()
  const location = useLocation()
  const functionData = location.state.functionData
  const languageExtension = location.state.languageExtension

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

  return (
      <div className={styles.content}>
        <h2>{languageIcons[languageExtension]} {"Функцияя".repeat(8)}</h2>
        <div className={styles.contentFlex}>
          <div className={styles.contentFlexLeft}>
            <FunctionDescription functionData={functionData} />
            <div className={styles.functionButtons}>
              <CiEdit title={"Редактировать"} onClick={editFunction}
                      className={styles.functionButton + " " + styles.editButton}/>
              <MdDeleteOutline title={"Удалить"} onClick={deleteFunction}
                               className={styles.functionButton + " " + styles.deleteButton}/>
            </div>
          </div>
          <LogsHistory />
        </div>

      </div>
  )
}