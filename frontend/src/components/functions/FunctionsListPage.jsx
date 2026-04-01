import styles from "../../css/FunctionsList.module.css"
import {useEffect, useState} from "react";
import {FunctionsList} from "./FunctionsList.jsx";
import {useNavigate} from "react-router";
import {HTTPMethods, httpRequest} from "../../utils/requests.js";

let allFunctions = []

export const FunctionsListPage = () => {

  const [displayedFunctions, setDisplayedFunctions] = useState(null)
  const navigate = useNavigate()

  const searchFunctions = (e) => {
    const input = e.target.value
    if (!input) {
      console.log(allFunctions)
      setDisplayedFunctions(allFunctions)
      return
    }
    setDisplayedFunctions(allFunctions.filter(f => {
      return (
          f.name.toLowerCase().startsWith(input) ||
          f.service.toLowerCase().startsWith(input) ||
          f.handlerPath.toLowerCase().startsWith(input) ||
          f.handler.toLowerCase().startsWith(input)
      )
    }))
  }

  useEffect(() => {
    httpRequest(HTTPMethods.GET, "/api/events/functions/get-all")
        .then((e) => {
          allFunctions = e.data
          setDisplayedFunctions(e.data)
        })
  }, []);

  const openProject = () => {
    navigate("../projects/1")
  }

  const createFunction = () => {
    navigate("create")
  }

  return (
      <div className={styles.content}>
        <h2 className={styles.projectName}>{"Проектт ".repeat(8)}</h2>
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