import styles from "../../css/StartPage.module.css"
import {ProjectsList} from "./ProjectsList.jsx";
import {ProjectDescription} from "./ProjectDescription.jsx";
import {useEffect, useState} from "react";
import {HTTPMethods, httpRequest} from "../../utils/requests.js";

export const StartPage = () => {

  const [isLoading, setIsLoading] = useState(true)
  const [clickedProject, setClickedProject] = useState(null)

  useEffect(() => {
    // httpRequest(HTTPMethods.GET, "/api/code/get-jwt-token").then(e => {
    //   const token = e.data["access_token"]
    //   if (token) {
    //     localStorage.setItem("accessToken", `Bearer ${token}`)
    //     console.log(localStorage.getItem("accessToken"))
    //     setIsLoading(false)
    //   }
    // }).catch(console.error)
    setIsLoading(false) // TODO временно
  }, []);

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

  if (isLoading)
    return <div className={styles.content}><span className={"loader dark"}></span></div>

  return (
    <div className={styles.content}>
      <ProjectsList setClickedProject={setClickedProject} />
      <ProjectDescription projectData={clickedProject} />
    </div>
  )
}