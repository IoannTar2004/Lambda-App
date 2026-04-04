import styles from "../../css/StartPage.module.css"
import {ProjectsList} from "./ProjectsList.jsx";
import {ProjectDescription} from "./ProjectDescription.jsx";
import {useEffect, useState} from "react";
import {HTTPMethods, httpRequest, printError} from "../../utils/requests.js";

export const StartPage = () => {

  const [isLoading, setIsLoading] = useState(true)
  const [clickedProject, setClickedProject] = useState(null)

  useEffect(() => {
    httpRequest(HTTPMethods.GET, "/api/code/auth/get-jwt-token", {userId: 300904}).then(e => {
      const token = e.data.accessToken
      if (token) {
        localStorage.setItem("accessToken", `Bearer ${token}`)
        setIsLoading(false)
      }
    }).catch(printError)
    setIsLoading(false) // TODO временно
  }, []);

  if (isLoading)
    return <div className={styles.content}><span className={"loader dark"}></span></div>

  return (
    <div className={styles.content}>
      <ProjectsList setClickedProject={setClickedProject} />
      <ProjectDescription projectData={clickedProject} />
    </div>
  )
}