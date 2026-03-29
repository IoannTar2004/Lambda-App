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
    const structure = ["a/ab/f2", "a/ab/f2/"]
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

  const handleDeleteClick = () => {
    setAction({type: "delete", path: contextMenu.path})
    setContextMenu(null)
  }

  const clearAction = () => setAction(null)

  const updatePath = (oldPath, newPath) => {
    setBaseStructure(prevState => {
      return prevState.map((path) => {
        console.log(path, oldPath)
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
    updatePath
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

              <div className={styles.actionBox}>
                <RiFileUploadFill className={".icon"}/> Загрузить файл
              </div>
              <div className={styles.actionBox}>
                <RiFileAddFill className={".icon"}/> Создать файл
              </div>
              <div className={styles.actionBox}>
                <FaFolderPlus className={".icon"}/> Создать папку
              </div>

              {contextMenu.path !== projectName + "/" && (
                <div className={styles.actionBox} onClick={handleDeleteClick}>
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
              <div className={styles.actionBox}>
                <MdDelete className={".icon"}/> Удалить
              </div>
            </div>
        )}
      </div>
  )
}