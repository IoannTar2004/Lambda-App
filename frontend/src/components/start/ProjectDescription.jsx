import styles from "../../css/StartPage.module.css"
import {useNavigate} from "react-router";

export const ProjectDescription = ({projectDescription}) => {

  const navigate = useNavigate()
  const languagesColors = {
    Python: "#3275AA",
    Java: "orangered",
    Other: "gray"
  }

  const setColor = () => {
    let linearGradient = "linear-gradient(to right"
    let totalPercent = 0
    for (let e of projectDescription) {
      console.log(e)
      const color = languagesColors[e.language]
      const percent = e.percent
      linearGradient += `, ${color} ${totalPercent}%, ${color} ${totalPercent + percent}%`
      totalPercent += percent
    }

    linearGradient += ")"
    return linearGradient
  }

  const openFunctionPage = () => {
    navigate("../functions")
  }

  const openProject = () => {
    navigate("../projects/1")
  }

  return (
      <div className={styles.projectDescBox}>
        <div className={styles.projectDescWindow}>
          <div className={styles.projectName}>{"Проектт ".repeat(8)}</div>
          <div className={styles.projectDesc}>Создан: {"26.03.2025 в 13:20"}</div>
          <div className={styles.projectDesc}>Последнее изменение: {"26.03.2025 в 13:20"}</div>

          <div className={styles.projectLanguageBarBox}>
            <div className={styles.bar} style={{background: setColor()}}>
            </div>
          </div>

          <div className={styles.languagesListBox}>
            {projectDescription.map(e =>
              <div className={styles.languageItem}>
                <div className={styles.languageCircle} style={{backgroundColor: languagesColors[e.language]}}></div>
                {e.language} ({e.percent}%)
              </div>
            )}
          </div>

          <div className={styles.projectButtonsBox}>
            <button id={styles.showFunctions} onClick={openFunctionPage}>Функции</button>
            <button id={styles.openProject} onClick={openProject}>Открыть проект</button>
          </div>
        </div>
      </div>
  )
}