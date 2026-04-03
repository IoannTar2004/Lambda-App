import styles from "../../css/FunctionsList.module.css"
import {useEffect, useRef, useState} from "react";
import {FunctionsList} from "./FunctionsList.jsx";
import {useLocation, useNavigate, useParams} from "react-router";
import {HTTPMethods, httpRequest, printError} from "../../utils/requests.js";

export const FunctionsListPage = () => {

  const {projectId} = useParams()
  const location = useLocation()
  const navigate = useNavigate()

  const [displayedFunctions, setDisplayedFunctions] = useState(null)
  const [projectName, setProjectName] = useState(null)

  const projectStructure = useRef([])
  const allFunctions = useRef(null)

  const searchFunctions = (e) => {
    const input = e.target.value
    if (!input) {
      setDisplayedFunctions(allFunctions.current)
      return
    }
    setDisplayedFunctions(allFunctions.current.filter(f => {
      return (
          f.name.toLowerCase().startsWith(input) ||
          f.service.toLowerCase().startsWith(input) ||
          f.handlerPath.toLowerCase().startsWith(input) ||
          f.handler.toLowerCase().startsWith(input)
      )
    }))
  }

  useEffect(() => {
    if (location?.state?.projectName)
      setProjectName(location.state.projectName)
    else
      httpRequest(HTTPMethods.GET, "/api/events/project/get-project", {projectId: projectId})
          .then(e => setProjectName(e.data.projectName))

    httpRequest(HTTPMethods.GET, "/api/events/functions/get-all", {projectId: projectId})
        .then((e) => {
          allFunctions.current = e.data
          setDisplayedFunctions(e.data)
        })
        .catch(printError)

    httpRequest(HTTPMethods.GET, "/api/code/user-files/listdir-all", {
      projectId: projectId,
      path: ""
    }).then((e) => {
      const project = e.data
      projectStructure.current = project.map(e => e.key.split("/").slice(2).join("/"))
    })
  }, []);

  const openProject = () => {
    navigate(`../projects/${projectId}/editor`)
  }

  const createFunction = () => {
    navigate("create", {
      state: {
        projectStructure: projectStructure.current
      }
    })
  }

  return (
      <div className={styles.content}>
        <h2 className={styles.projectName}>{projectName}</h2>
        <div className={styles.openProjectBox}>
          <button id={styles.openProject} onClick={openProject}>Открыть проект</button>
        </div>

        <div className={styles.toolsBox}>
          <div className={styles.searchInputBox}>
            <input id={styles.searchInput} placeholder={"Поиск"} onChange={searchFunctions}/>
          </div>
          <div className={styles.createFunctionButtonBox}>
            <button id={styles.createFunction} onClick={createFunction}>Создать функцию</button>
          </div>
        </div>
          <FunctionsList functions={displayedFunctions} />
      </div>
  )
}