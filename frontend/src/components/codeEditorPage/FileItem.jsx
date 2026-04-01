import styles from "../../css/CodeEditor.module.css";
import {FaFile} from "react-icons/fa";
import {languageExtensionIcons} from "../functions/LanguageIcons.jsx";
import {useContext, useEffect, useRef, useState} from "react";
import {ProjectContext} from "./ProjectStructure.jsx";
import {FileContext} from "./CodeEditorPage.jsx";
import {httpRequest, httpRequestFormData} from "../../utils/requests.js";
import {useParams} from "react-router";

export const FileItem = ({currentPath}) => {

  const extension = currentPath.split(".").pop()
  const correctNamePattern = /^[а-яА-Я\w.-]+$/

  const {id} = useParams()
  const { action, clearAction, setContextMenu, updatePath } = useContext(ProjectContext);
  const [name, setName] = useState(currentPath.split("/").pop())
  const [isRenaming, setIsRenaming] = useState(false)
  const [uploadBuffer, setUploadBuffer] = useState(null)
  const {currentFile, setCurrentFile} = useContext(FileContext)

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
    if (action?.path === currentPath) {
      if (action?.type === "rename")
        setIsRenaming(true)
      else if (action?.type === "createFile") {
        setName("")
        setIsRenaming(true)
      }
      else if (action?.type === "uploadFile")
        setUploadBuffer(action?.text)
    }

  }, [action, currentPath]);

  const finishRename = () => {
    const oldName = currentPath.split("/").pop()
    if (oldName === name) {
      setIsRenaming(false);
      clearAction();
      return;
    }
    if (!correctNamePattern.test(name)) {
      handleOnBlur()
      return;
    }

    const parentPath = currentPath.substring(0, currentPath.lastIndexOf('/'));
    const newPath = parentPath ? `${parentPath}/${name}` : name;
    if (action?.type === "createFile") {
      const createdFile = new File([""], name, { type: 'text/plain' });

      httpRequestFormData("/api/code/user-files/upload-file", {
        projectId: id,
        file: createdFile,
        directory: parentPath
      }).then(() => {
        setCurrentFile({name: newPath, upload: " "})
        updatePath(currentPath, newPath);
        setIsRenaming(false);
        clearAction()
      })

      return;
    }

    updatePath(currentPath, newPath);
    setIsRenaming(false);
    clearAction()
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

  const handleOnClick = () => {
    setCurrentFile({name: currentPath, upload: uploadBuffer})
    setUploadBuffer(null)
  }

  return (
      <div className={styles.directory} style={{marginLeft: `20px`}}>
        <div className={styles.directoryHeader} onContextMenu={openContextMenu} onClick={handleOnClick}>
          <div>
            <span>{languageExtensionIcons[extension] || <FaFile className={"icon"}/>} </span>
            {isRenaming ?
              <input className={styles.rename} autoFocus value={name} size={name.length || 1} onKeyDown={handleKeyDown}
                     onChange={(e) => {setName(e.target.value)}}
                     onBlur={handleOnBlur}
                     style={{backgroundColor: !correctNamePattern.test(name) ? "#F66A6AFF" : ""}}/> :
              <span className={styles.name}>{name}</span>
            }
          </div>
        </div>
      </div>
  )
}