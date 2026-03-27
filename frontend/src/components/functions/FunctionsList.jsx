import styles from "../../css/FunctionsList.module.css";
import {useNavigate} from "react-router";
import {languageIcons} from "./LanguageIcons.jsx";

export const FunctionsList = ({functions}) => {

  const navigate = useNavigate()

  const openFunction = (data, extension) => {
    navigate(`${data.id}`, {
      state: {
        functionData: data,
        languageExtension: extension
      }
    })
  }

  return (
      <div className={styles.functionsListBox}>
          {functions.map(e => {
              const extension = e.handlerPath.split('.').pop()
              return (
                  <div className={styles.functionElement} onClick={() => openFunction(e, extension)}>
                    <div className={styles.name}>{e.name}</div>

                    <div className={styles.info}><span>Сервис: </span>{e.service}</div>
                    <div className={styles.info}><span>Путь к обработчику: </span>
                      {languageIcons[extension]} {e.handlerPath}
                    </div>
                    <div className={styles.info}><span>Обработчик: </span> {e.handler}</div>
                  </div>
              )

            }

          )}

        </div>
  )
}