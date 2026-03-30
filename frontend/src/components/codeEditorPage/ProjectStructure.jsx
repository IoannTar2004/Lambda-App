import styles from "../../css/CodeEditor.module.css";
import {createContext, use, useEffect, useMemo, useState} from "react";
import {Directory} from "./Directory.jsx";
import {RiFileAddFill, RiFileUploadFill} from "react-icons/ri";
import {FaFolderPlus} from "react-icons/fa";
import {MdDelete, MdDriveFileRenameOutline} from "react-icons/md";
import {useParams} from "react-router";


export const ProjectContext = createContext(null)
//["a/ab/f1.py", "a/ab/f2.py", "a/f1.py", "b/f1.py", "c/", "a1.js", "a2.py"]
export const ProjectStructure = () => {

  const {id} = useParams()
  const [loading, setLoading] = useState(true)
  const [projectName, setProjectName] = useState("")
  const [baseStructure, setBaseStructure] = useState([])
  const [contextMenu, setContextMenu] = useState(null)
  const [action, setAction] = useState(null)

  useEffect(() => {
    const structure = ["a/ab/f1.py", "a/ab/f2.py", "a/f1.py", "b/f1.py", "c/", "a1.js", "a2.py"]
    setProjectName("my_project")
    setBaseStructure(structure)
    setLoading(false)
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

  const handleRenameClick = () => {
    setAction({type: "rename", path: contextMenu.path})
    setContextMenu(null)
  }

  const checkPath = (path, prefix) => {
    return path === prefix || prefix.endsWith("/") && path.startsWith(prefix)
  }

  const handleDeleteDirectoryClick = () => {
    const deletePath = contextMenu.path
    const split = deletePath.split("/")
    const last = split[split.length - 1] === "" ? 2 : 1
    const parent = split.slice(0, split.length - last).join("/") + "/"
    const countParent = baseStructure.reduce((acc, path) => acc + (checkPath(path, parent) ? 1 : 0), 0)
    const countDeletePath = baseStructure.reduce((acc, path) => acc + (checkPath(path, deletePath) ? 1 : 0), 0)

    if (countParent === countDeletePath) {
      let deleteStructure = [...baseStructure]
      const index = deleteStructure.findIndex(path => checkPath(path, parent))
      deleteStructure[index] = parent
      deleteStructure = deleteStructure.filter((path, i) => i === index || !checkPath(path, deletePath))
      setBaseStructure(deleteStructure)
    }
    else {
      setBaseStructure(prevState => {
        return prevState.filter((path) => !checkPath(path, deletePath))
      })
    }

    setContextMenu(null)
  }

  const handleCreateFile = () => {
    const path = contextMenu.path === projectName + "/" ? "" : contextMenu.path
    const newFile= path + ".new"
    setBaseStructure(prevState => {
      prevState.push(newFile)
      return prevState
    })

    setAction({type: "createFile", path: newFile, dir: path})
    setContextMenu(null)
  }

  const handleCreateFolder = () => {
    const path = contextMenu.path === projectName + "/" ? "" : contextMenu.path
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

    const reader = new FileReader()
    reader.onload = (e) => {
      const content = e.target.result
      console.log(content)
    }
    reader.onerror = () => {
      alert("Ошибка при чтении")
    }

    reader.readAsText(file)
    event.target.value = '';

    setAction({type: "createFile", dir: contextMenu.path})

    setBaseStructure(prevState => {
      prevState.push(contextMenu.path + file.name)
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

  if (loading)
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
              {contextMenu.path !== projectName + "/" && (
                <div className={styles.actionBox} onClick={handleRenameClick}>
                  <MdDriveFileRenameOutline className={".icon"}/> Переименовать
                </div>
              )}

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

              {contextMenu.path !== projectName + "/" && (
                <div className={styles.actionBox} onClick={handleDeleteDirectoryClick}>
                  <MdDelete className={".icon"}/> Удалить
                </div>
              )}

            </div>
        )}

        {contextMenu?.type === "File" && (
            <div className={styles.contextMenu} style={{top: contextMenu.y, left: contextMenu.x}}>
              <div className={styles.actionBox} onClick={handleRenameClick}>
                <MdDriveFileRenameOutline className={".icon"}/> Переименовать
              </div>
              <div className={styles.actionBox} onClick={handleDeleteDirectoryClick}>
                <MdDelete className={".icon"}/> Удалить
              </div>
            </div>
        )}
      </div>
  )
}