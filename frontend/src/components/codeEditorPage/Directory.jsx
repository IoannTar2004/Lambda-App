import styles from "../../css/CodeEditor.module.css";
import {FaFolder, FaFolderOpen} from "react-icons/fa";
import {useContext, useEffect, useState} from "react";
import {FileItem} from "./FileItem.jsx";
import {ProjectContext} from "./ProjectStructure.jsx";

export const Directory = ({level, currentPath, content}) => {

  const correctNamePattern = /^[а-яА-Я\w.-]+$/

  const [opened, setOpened] = useState(level === 0)
  const { action, clearAction, setContextMenu, updatePath } = useContext(ProjectContext);
  const [name, setName] = useState(currentPath.split("/").slice(-2, -1))
  const [isRenaming, setIsRenaming] = useState(false)

  useEffect(() => {
    if (action?.type === "rename" && action?.path === currentPath) {
      setIsRenaming(true)
    }
  }, [action, currentPath]);

  const buildStructure = () => {
    const childrenMap = new Map()
    for (let path of content) {
      const split = path.split("/")
      const name = split[0] + (split.length > 1 ? "/" : "")
      if (!childrenMap.has(name))
        childrenMap.set(name, [])
      if (split.length > 1) {
        const restPath = split.slice(1).join("/")
        childrenMap.get(name).push(restPath)
      } else {
        childrenMap.get(name).push(null)
      }
    }

    return Array.from(childrenMap.entries()).map(([name, childContent]) => {
      name = name[name.length - 1] === "/" ? name.slice(0, name.length - 1) : name
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
      path: currentPath,
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
    updatePath(currentPath, newPath);

    setIsRenaming(false);
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
        <div className={styles.directoryHeader} onClick={() => {
          setOpened(!opened)
          // console.log(currentPath)
        }} onContextMenu={openContextMenu}>
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