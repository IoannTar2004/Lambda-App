import styles from "../../css/FunctionsList.module.css"
import {useEffect, useState} from "react";
import {FunctionsList} from "./FunctionsList.jsx";
import {useNavigate} from "react-router";

export const FunctionsListPage = () => {

  let allFunctions = []

  for (let i = 0; i < 10; i++) {
      allFunctions[i] = {
        id: i,
        name: "Функция " + i,
        service: "Хранилище S3 " + i,
        handlerPath: `test_script_${i}.py`,
        handler: "print_message" + i
    }
  }

  const [displayedFunctions, setDisplayedFunctions] = useState([])
  const navigate = useNavigate()

  const searchFunctions = (e) => {
    const input = e.target.value
    if (!input) {
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
    setDisplayedFunctions(allFunctions)
  }, []);

  const openProject = () => {
    navigate("../projects/1")
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
            <button id={styles.createFunction}>Создать функцию</button>
          </div>
        </div>

        <FunctionsList functions={displayedFunctions} />
      </div>
  )
}