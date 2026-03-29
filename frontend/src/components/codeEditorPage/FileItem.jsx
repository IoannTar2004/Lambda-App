import styles from "../../css/CodeEditor.module.css";
import {FaFile} from "react-icons/fa";
import {languageIcons} from "../functions/LanguageIcons.jsx";
import {useContext, useEffect, useRef, useState} from "react";
import {ProjectContext} from "./ProjectStructure.jsx";

export const FileItem = ({currentPath}) => {

  const extension = currentPath.split(".").pop()
  const { action, clearAction, setContextMenu, updatePath } = useContext(ProjectContext);
  const [name, setName] = useState(currentPath.split("/").pop())
  const [isRenaming, setIsRenaming] = useState(false)

  const openContextMenu = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setContextMenu({x: e.clientX,
      y: e.clientY,
      path: currentPath,
      type: "File"}
    )
  }

  useEffect(() => {
    if (action?.type === "rename" && action?.path === currentPath) {
      setIsRenaming(true)
    }
  }, [action, currentPath]);

  const finishRename = () => {
    const oldName = currentPath.split("/").pop()
    if (oldName === name) {
      setIsRenaming(false);
      clearAction();
      return;
    }
    if (name === "") {
      handleOnBlur()
      return;
    }

    const parentPath = currentPath.substring(0, currentPath.lastIndexOf('/'));
    const newPath = parentPath ? `${parentPath}/${name}` : name;
    updatePath(currentPath, newPath);

    setIsRenaming(false);
  }

  const handleOnBlur = () => {
    setName(currentPath.split("/").pop())
    setIsRenaming(false);
    clearAction();
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter")
      finishRename()
    if (e.key === "Escape") {
      setName(currentPath.split("/").pop())
      setIsRenaming(false)
      clearAction()
    }
  }

  return (
      <div className={styles.directory} style={{marginLeft: `20px`}}>
        <div className={styles.directoryHeader} onContextMenu={openContextMenu} onClick={() => console.log(currentPath)}>
          <div>
            <span>{languageIcons[extension] || <FaFile className={"icon"}/>} </span>
            {isRenaming ?
              <input className={styles.rename} autoFocus value={name} size={name.length || 1} onKeyDown={handleKeyDown}
                     onChange={(e) => {setName(e.target.value)}}
                     onBlur={handleOnBlur}
                     style={{backgroundColor: name === "" ? "#F66A6AFF" : ""}}/> :
              <span className={styles.name}>{name}</span>
            }
          </div>
        </div>
      </div>
  )
}