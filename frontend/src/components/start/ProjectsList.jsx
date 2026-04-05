import styles from "../../css/StartPage.module.css"
import {useEffect, useState} from "react";
import {useNavigate} from "react-router";
import {HTTPMethods, httpRequest} from "../../utils/requests.js";

export const ProjectsList = ({setClickedProject}) => {

  const navigate = useNavigate()

  const [projects, setProjects] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    httpRequest(HTTPMethods.GET, "/api/events/project/get-projects")
        .then(e => {
          setProjects(e.data)
          setIsLoading(false)
        }).catch(console.error)
  }, []);

  const createProject = () => {
    navigate("create-project")
  }

  const clickOnProject = (projectData) => {
    setClickedProject(projectData)
  }

  if (isLoading)
    return (
        <div className={styles.projectsBox}>
          <div className={styles.projectsListBox} style={{marginTop: "25%"}}>
            <span className={"loader dark"}></span>
          </div>
        </div>)

  return (
      <div className={styles.projectsBox}>
        <h3>Проекты</h3>
        <button className={styles.createProject} onClick={createProject}>Создать проект</button>
        <div className={styles.projectsListBox}>
          {projects.length > 0 ? (projects.map((e) =>
              <div key={e.id} className={styles.projectElement} onClick={() => clickOnProject(e)}>
                <div className={styles.projectName}>{e.projectName}</div>
                <div className={styles.projectDesc}>{"26.03.2025 в 13:20"}</div>
              </div>)
            ) : (
              <div className={styles.noData}>Создайте свой первый проект!</div>
          )}
        </div>
      </div>
  )
}