import functionStyles from "../../css/Function.module.css";
import styles from "../../css/StartPage.module.css"
import {useState} from "react";
import {HTTPMethods, httpRequest} from "../../utils/requests.js";
import {HttpStatusCode} from "axios";
import {useNavigate} from "react-router";

export const CreateProjectPage = () => {

  const navigate = useNavigate()
  const [error, setError] = useState()
  const [name, setName] = useState("")

  const handleCreateProject = () => {
    httpRequest(HTTPMethods.POST, "/api/events/project/create", {
      projectName: name
    }).then(e => {
      const id = e.data.id
      navigate("../projects/" + id)
    }).catch((err) => {
      if (err.status === HttpStatusCode.Conflict)
        setError("Проект с таким названием уже существует!")
    })
  }

  return (
    <div className={functionStyles.modalContent}>
      <div className={functionStyles.formWindow + " " + functionStyles.center}>
        <input placeholder={"Название проекта"} minLength={3} maxLength={64} onFocus={() => setError("")}
               onChange={e => setName(e.target.value)}/>
        <div className={"error"}>{error}</div>
        <button className={styles.createProject} onClick={handleCreateProject}>Создать</button>
      </div>
    </div>
  )
}