import styles from "../../css/StartPage.module.css"
import {ProjectsList} from "./ProjectsList.jsx";

export const StartPage = () => {
  return (
      <div className={styles.content}>
        <ProjectsList />
          <div className={styles.projectsBox2}>
        </div>
      </div>
  )
}