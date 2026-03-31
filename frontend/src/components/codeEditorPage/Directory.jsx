import styles from "../../css/CodeEditor.module.css";
import {FaFolder, FaFolderOpen} from "react-icons/fa";
import {useContext, useEffect, useState} from "react";
import {FileItem} from "./FileItem.jsx";
import {ProjectContext} from "./ProjectStructure.jsx";
import {httpRequestFormData} from "../../utils/requests.js";
import {useParams} from "react-router";
import {isReservedName} from "../../utils/reservedFiles.js";

export const Directory = ({level, currentPath, content}) => {

  const correctNamePattern = /^[а-яА-Я\w.-]+$/

  const {id} = useParams()
  const [opened, setOpened] = useState(level === 0)
  const { action, clearAction, setContextMenu, updatePath } = useContext(ProjectContext);
  const [name, setName] = useState(currentPath.split("/").slice(-2, -1))
  const [isRenaming, setIsRenaming] = useState(false)

   useEffect(() => {
     if (action?.type === "rename" && action?.path === currentPath)
       setIsRenaming(true)
     if (["createFile", "createFolder", "uploadFile"].includes(action?.type) && action?.dir === currentPath)
       setOpened(true)
     if (action?.type === "createFolder" && action?.path === currentPath) {
       setName("")
       setIsRenaming(true)
     }

  }, [action, currentPath]);

  const buildStructure = () => {
    const childrenMap = new Map()
    for (let path of content) {
      const split = path.split("/")
      const name = split[0] + (split.length > 1 ? "/" : "")

      if (isReservedName(name)) continue

      if (!childrenMap.has(name))
        childrenMap.set(name, [])
      if (split.length > 1) {
        const restPath = split.slice(1).join("/")
        childrenMap.get(name).push(restPath)
      } else {
        childrenMap.get(name).push(null)
      }
    }
    const sortedKeys = Array.from(childrenMap.keys()).sort((a, b) => {
      const aIsDir = a.endsWith('/');
      const bIsDir = b.endsWith('/');

      if (aIsDir && !bIsDir) return -1;
      if (!aIsDir && bIsDir) return 1;

      return a.localeCompare(b);
    });

    return sortedKeys.map(key => {
      const childContent = childrenMap.get(key);
      const name = key.endsWith('/') ? key.slice(0, -1) : key;
      if (name === "")
        return null

      const isFile = childContent[0] === null
      const newPath = `${level > 0 ? currentPath : ""}${name}`
      if (isFile)
        return <FileItem key={newPath} currentPath={newPath}/>

      return <Directory key={newPath + "/"} level={level + 1} currentPath={newPath + "/"} content={childContent} />
    })
  }

  const openContextMenu = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setContextMenu({x: e.clientX,
      y: e.clientY,
      path: level > 0 ? currentPath : "",
      type: "Directory"}
    )
  }

  const finishRename = () => {
    const split = currentPath.split("/")
    const oldName = split[split.length - 2]
    if (oldName === name) {
      setIsRenaming(false);
      clearAction();
      return;
    }
    if (!correctNamePattern.test(name)) {
      setName(split[split.length - 2])
      setIsRenaming(false);
      clearAction();
      return;
    }

    split[split.length - 2] = name
    const newPath = split.join("/");

    if (action?.type === "createFolder") {
      const createdFile = new File([""], ".dir", { type: 'text/plain' });
      httpRequestFormData("/api/code/user-files/upload-file", {
        projectId: id,
        file: createdFile,
        directory: newPath
      }).then(() => {
        updatePath(currentPath, newPath)
        setIsRenaming(false);
        clearAction()
      })
    }
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
      <div className={styles.directory} style={{marginLeft: `${level === 0 ? 0 : 20}px`}}>
        <div className={styles.directoryHeader} onClick={() => setOpened(!opened)} onContextMenu={openContextMenu}>
          <div>
            {opened ?
              <span><FaFolderOpen className={"icon"} size={"20px"}/></span> :
              <span><FaFolder className={"icon"} size={"20px"}/> </span>
            }
            {isRenaming ?
              <input className={styles.rename} autoFocus value={name} size={name.length || 1} onKeyDown={handleKeyDown}
                     onChange={(e) => {setName(e.target.value)}}
                     style={{backgroundColor: !correctNamePattern.test(name) ? "#F66A6AFF" : ""}}/> :
              <span className={styles.name}>{name}</span>
            }
          </div>
        </div>
        {opened && buildStructure()}
      </div>

  )
}