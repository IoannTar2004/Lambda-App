import styles from "../../css/CodeEditor.module.css";
import {createContext, use, useContext, useEffect, useMemo, useState} from "react";
import {Directory} from "./Directory.jsx";
import {RiFileAddFill, RiFileUploadFill} from "react-icons/ri";
import {FaFolderPlus} from "react-icons/fa";
import {MdDelete, MdDriveFileRenameOutline} from "react-icons/md";
import {useLocation, useNavigate, useParams} from "react-router";
import {HTTPMethods, httpRequest, httpRequestFormData} from "../../utils/requests.js";
import {FileContext} from "./CodeEditorPage.jsx";


export const ProjectContext = createContext(null)
export const ProjectStructure = () => {

  const {id} = useParams()
  const {currentFile, setCurrentFile} = useContext(FileContext)
  const [isLoading, setIsLoading] = useState(true)
  const [projectName, setProjectName] = useState("")
  const [baseStructure, setBaseStructure] = useState([])
  const [contextMenu, setContextMenu] = useState(null)
  const [action, setAction] = useState(null)

  useEffect(() => {
    httpRequest(HTTPMethods.GET, "/api/events/project/get-project", {projectId: id})
        .then(e => {
          const project = e.data
          setProjectName(project.projectName)
          httpRequest(HTTPMethods.GET, "/api/code/user-files/listdir-all", {
            projectId: id,
            path: ""
          }).then(s => {
            const getStructure = s.data.map(e => e.key.split("/").slice(2).join("/"))
            setBaseStructure(getStructure)
            setIsLoading(false)
          })
        })

  }, []);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest(`.${styles.contextMenu}`)) {
        setContextMenu(null);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [contextMenu]);

  //TODO реализовать переименование
  const handleRenameClick = () => {
    setAction({type: "rename", path: contextMenu.path})
    setContextMenu(null)
  }

  const checkPath = (path, prefix) => {
    return path === prefix || prefix.endsWith("/") && path.startsWith(prefix)
  }

  const handleDeleteClick = () => {
    const deletePath = contextMenu.path
    const deleteKeys = baseStructure.filter((path) => checkPath(path, deletePath))
    httpRequest(HTTPMethods.DELETE, "/api/code/user-files/delete", {
      projectId: id,
      keys: deleteKeys
    }).then(() => {
      if (currentFile?.name && checkPath(currentFile.name, contextMenu.path))
        setCurrentFile(null)
      setBaseStructure(prevState => {
        return prevState.filter((path) => !checkPath(path, deletePath))
      })

    })

    setContextMenu(null)
  }

  const getPathNoProject = (path) => path === projectName + "/" ? "" : path

  const handleCreateFile = () => {
    const path = getPathNoProject(contextMenu.path)
    const newFile= path + ".new"
    setBaseStructure(prevState => {
      prevState.push(newFile)
      return prevState
    })

    setAction({type: "createFile", path: newFile, dir: path})
    setContextMenu(null)
  }

  const handleCreateFolder = () => {
    const path = getPathNoProject(contextMenu.path)
    const newFolder = path + "new/"
    setBaseStructure(prevState => {
      prevState.push(newFolder)
      return prevState
    })
    setAction({type: "createFolder", path: newFolder, dir: path})
    setContextMenu(null)
  }

  const handleUploadFile = (event) => {
    const file = event.target.files[0]
    const path = getPathNoProject(contextMenu.path) + file.name
    const reader = new FileReader()
    reader.onload = (e) => {
      httpRequestFormData("/api/code/user-files/upload-file", {
        projectId: id,
        file: file,
        directory: contextMenu.path
      }).then()

      const content = e.target.result
      setAction({type: "uploadFile", dir: contextMenu.path, path: path, text: content})
    }

    reader.onerror = () => {
      alert("Ошибка при чтении")
    }

    reader.readAsText(file)
    event.target.value = '';


    setBaseStructure(prevState => {
      prevState.push(path)
      return prevState
    })
    setContextMenu(null)
  }


  const clearAction = () => setAction(null)

  const updatePath = (oldPath, newPath) => {
    setBaseStructure(prevState => {
      return prevState.map((path) => {
        if (path === oldPath || oldPath.endsWith("/") && path.startsWith(oldPath)) {
          const relativePart = path.slice(oldPath.length);
          return newPath + relativePart;
        }
        return path
      })
    })
  }

  const contextValue = useMemo(() => ({
    action,
    clearAction,
    setContextMenu,
    updatePath,
  }), [action]);

  if (isLoading)
    return (
        <div className={styles.projectStructureBox}>
          <span className={"loader"}></span>
        </div>
      )

  return (
      <div className={styles.projectStructureBox}>
        <ProjectContext.Provider value={contextValue}>
          <Directory level={0} currentPath={projectName + "/"} content={baseStructure} />
        </ProjectContext.Provider>

        {contextMenu?.type === "Directory" && (
            <div className={styles.contextMenu} style={{top: contextMenu.y, left: contextMenu.x}}>

              <div className={styles.actionBox + " " + styles.uploadFile} onChange={handleUploadFile}>
                <RiFileUploadFill className={".icon"}/> Загрузить файл
                <input type={"file"}/>
              </div>
              <div className={styles.actionBox} onClick={handleCreateFile}>
                <RiFileAddFill className={".icon"}/> Создать файл
              </div>
              <div className={styles.actionBox} onClick={handleCreateFolder}>
                <FaFolderPlus className={".icon"}/> Создать папку
              </div>

              {contextMenu.path !== "" && (
                <div className={styles.actionBox} onClick={handleDeleteClick}>
                  <MdDelete className={".icon"}/> Удалить
                </div>
              )}

            </div>
        )}

        {contextMenu?.type === "File" && (
            <div className={styles.contextMenu} style={{top: contextMenu.y, left: contextMenu.x}}>
              <div className={styles.actionBox} onClick={handleDeleteClick}>
                <MdDelete className={".icon"}/> Удалить
              </div>
            </div>
        )}
      </div>
  )
}