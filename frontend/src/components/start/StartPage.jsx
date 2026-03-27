import styles from "../../css/StartPage.module.css"
import {ProjectsList} from "./ProjectsList.jsx";
import {ProjectDescription} from "./ProjectDescription.jsx";

export const StartPage = () => {
  const projectDescription = [
      {
        language: "Python",
        percent: 60
      },
      {
        language: "Java",
        percent: 38
      },
      {
        language: "Other",
        percent: 2
      }
  ]

  return (
      <div className={styles.content}>
        <ProjectsList />
        <ProjectDescription projectDescription={projectDescription} />
      </div>
  )
}