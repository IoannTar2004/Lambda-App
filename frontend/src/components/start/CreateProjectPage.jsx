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
  const [isProcessing, setIsProcessing] = useState(false)

  const handleCreateProject = () => {
    if (name.length < 3) {
      setError("В названии проекта должно быть минимум 3 символа")
      return
    }
    setIsProcessing(true)

    httpRequest(HTTPMethods.POST, "/api/events/project/create", {
      projectName: name
    }).then(e => {
      const id = e.data.projectId
      navigate(`../projects/${id}/editor`)
    }).catch((err) => {
      if (err.status === HttpStatusCode.Conflict)
        setError("Проект с таким названием уже существует!")
      setIsProcessing(false)
    })
  }

  if (isProcessing)
    return (<div className={functionStyles.modalContent}><span className={"loader dark"}></span></div>)

  return (
    <div className={functionStyles.modalContent}>
      <div className={functionStyles.formWindow + " " + functionStyles.center}>
        <input value={name} placeholder={"Название проекта"} minLength={3} maxLength={64} onFocus={() => setError("")}
               onChange={e => setName(e.target.value)}/>
        <div className={"error"}>{error}</div>
        <button className={styles.createProject} onClick={handleCreateProject}>Создать</button>
      </div>
    </div>
  )
}