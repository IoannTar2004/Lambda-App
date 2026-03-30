import functionStyles from "../../css/Function.module.css";
import styles from "../../css/StartPage.module.css"
import {useState} from "react";

export const CreateProjectPage = () => {

  const [error, setError] = useState()
  const [name, setName] = useState("")

  const handleCreateProject = () => {
    setError("Проект с таким названием уже существует!")
  }

  return (
    <div className={functionStyles.modalContent}>
      <div className={functionStyles.formWindow + " " + functionStyles.center}>
        <input placeholder={"Название проекта"} minLength={3} maxLength={64} onChange={e => setName(e.target.value)}/>
        <div className={"error"}>{error}</div>
        <button className={styles.createProject} onClick={handleCreateProject}>Создать</button>
      </div>
    </div>
  )
}