import styles from "../../css/StartPage.module.css"
import {useNavigate} from "react-router";
import {useContext, useEffect, useState} from "react";
import {IoCodeSlash} from "react-icons/io5";
import {HTTPMethods, httpRequest} from "../../utils/requests.js";
import {languages} from "../../utils/languages.js";
import {isReservedFile} from "../../utils/reserved.js";
import {getStringDate} from "../../utils/formats.js";

const projectDescriptionCache = new Map()

export const ProjectDescription = ({projectData}) => {

  const navigate = useNavigate()
  const [projectDescription, setProjectDescription] = useState({
    lastModified: null,
    languages: null
  })

  const countFiles = (files) => {
    let lastModified = 0
    const filesExtension = {}

    for (let f of files) {
      if (isReservedFile(f.key.split("/").pop()))
        continue

      lastModified = Math.max(new Date(f.lastModified).getTime(), lastModified)
      const extension = f.key.split('.').pop()

      if (!extension || f.key.endsWith('/')) continue;

      if (!filesExtension.hasOwnProperty(extension))
        filesExtension[extension] = 1
      else
        filesExtension[extension] += 1
    }

    const languagesPercents = []
    for (let e in filesExtension) {
      let language = languages[e] || "Other"
      const percent = Math.round((filesExtension[e] / files.length) * 1000) / 10
      languagesPercents.push({language: language, percent: percent})
    }

    languagesPercents.sort((a, b) => b.percent - a.percent)

    const data = {
      ...projectData,
      lastModified: files.length > 0 ? lastModified : null,
      languages: languagesPercents
    }
    setProjectDescription(data)
    projectDescriptionCache.set(projectData.id, data)
    console.log(lastModified)
    // const data = new Date(files[0].lastModified).getTime()

  }

  useEffect(() => {
    if (!projectData)
      return

    if (projectDescriptionCache.has(projectData.id))
      setProjectDescription(projectDescriptionCache.get(projectData.id))
    else {
      setProjectDescription({...projectDescription, languages: null})
      httpRequest(HTTPMethods.GET, "/api/code/user-files/listdir-all", {
        projectId: projectData.id,
        path: ""
      }).then(e => countFiles(e.data)).catch(console.error)
    }

  }, [projectData]);

  const languagesColors = {
    Python: "#3275AA",
    Java: "orangered",
    JavaScript: "yellow",
    Other: "gray"
  }

  const setLanguageBar = () => {
    if (projectDescription.languages.length === 0)
      return ""

    let linearGradient = "linear-gradient(to right"
    let totalPercent = 0
    for (let e of projectDescription.languages) {
      const color = languagesColors[e.language]
      const percent = e.percent
      linearGradient += `, ${color} ${totalPercent}%, ${color} ${totalPercent + percent}%`
      totalPercent += percent
    }
    linearGradient += ")"
    return linearGradient
  }

  const openFunctionPage = () => {
    navigate(`../projects/${projectData.id}/functions`, {
      state: {
        projectName: projectData.projectName
      }
    })
  }

  const openProject = () => {
    navigate(`../projects/${projectData.id}/editor`)
  }

  if (!projectData)
    return (
      <div className={styles.projectDescBox}>
        <div className={styles.projectDescWindow}>
          <div className={styles.noData}>
            <IoCodeSlash size={"50px"} />
            <h3>Здесь будет выведена информация о проекте</h3>
          </div>
        </div>
      </div>
    )

  //TODO исправить время создания и последнего изменения
  return (
      <div className={styles.projectDescBox}>
        <div className={styles.projectDescWindow}>
          <div className={styles.projectName}>{projectData.projectName}</div>
          <div className={styles.projectDesc}>Создан: {"26.03.2025 в 13:20"}</div>
          <div className={styles.projectDesc}>Последнее изменение: {
            projectDescription.lastModified ? getStringDate(projectDescription.lastModified) : ""}</div>

          {projectDescription.languages ? (
            <>
              <div className={styles.projectLanguageBarBox}>
                <div className={styles.bar} style={{background: setLanguageBar()}}></div>
              </div>

              <div className={styles.languagesListBox}>
                {projectDescription.languages.length === 0 && <div style={{fontSize: "20px"}}>
                  Отсутствуют файлы с расширениями
                </div>}

                {projectDescription.languages.map(e =>
                  <div className={styles.languageItem}>
                    <div className={styles.languageCircle} style={{backgroundColor: languagesColors[e.language]}}></div>
                    {e.language} ({e.percent}%)
                  </div>
                )}
              </div>
            </>
          ) : (
              <div className={styles.languagesListBox}>
                <span className={"loader dark"}></span>
              </div>
          )}

          <div className={styles.projectButtonsBox}>
            <button id={styles.showFunctions} onClick={openFunctionPage}>Функции</button>
            <button id={styles.openProject} onClick={openProject}>Открыть проект</button>
          </div>
        </div>
      </div>
  )
}