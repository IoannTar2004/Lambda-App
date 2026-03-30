import styles from "../../css/StartPage.module.css"
import {useEffect, useState} from "react";
import {useNavigate} from "react-router";

export const ProjectsList = () => {

  const navigate = useNavigate()

  const [projects, setProjects] = useState([])

  useEffect(() => {
    const newProjects = Array(15).fill({
      name: "Проект ".repeat(7),
      modified: "26.03.2025 в 13:20"
    })
    setProjects(newProjects)
  }, []);

  const createProject = () => {
    navigate("create-project")
  }

  return (
      <div className={styles.projectsBox}>
        <h3>Проекты</h3>
        <button className={styles.createProject} onClick={createProject}>Создать проект</button>
        <div className={styles.projectsListBox}>
          {projects.length > 0 ? (projects.map((e) =>
              <div className={styles.projectElement}>
                <div className={styles.projectName}>{e.name}</div>
                <div className={styles.projectDesc}>{e.modified}</div>
              </div>)
            ) : (
              <div className={styles.noProjects}>Создайте свой первый проект!</div>
          )}
        </div>
      </div>
  )
}