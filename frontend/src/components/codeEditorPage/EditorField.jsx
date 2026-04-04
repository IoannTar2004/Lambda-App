import Editor from "@monaco-editor/react";
import {Fragment, useContext, useEffect, useRef, useState} from "react";
import axios from "axios";
import styles from "../../css/CodeEditor.module.css";
import {FileContext} from "./CodeEditorPage.jsx";
import {languages} from "../../utils/languages.js";
import {HTTPMethods, httpRequest, httpRequestFormData} from "../../utils/requests.js";
import {useParams} from "react-router";

export const EditorField = ({globalContextMenu, setGlobalContextMenu}) => {

  const {id} = useParams()
  const {currentFile, setCurrentFile} = useContext(FileContext)

  const fileCache = useRef(new Map())
  const editorRef = useRef(null);
  const saveButtonRef = useRef(null)
  const isProcessing = useRef(false)

  useEffect(() => {
    if (!editorRef.current || !currentFile) return

    const name = currentFile.name

    if (currentFile.upload)
      editorRef.current.setValue(currentFile.upload)

    else if (!fileCache.current.has(name)) {
      httpRequest(HTTPMethods.GET, "/api/code/user-files/download-file", {
        projectId: id,
        path: name
      }).then((e) => {
        fileCache.current.set(name, true)
        editorRef.current.setValue(e.data)
      })
    }

    fileCache.current.set(name, true)

  }, [currentFile]);

  const editorOnMountEvent = (e) => {
    editorRef.current = e
  }

  const handleSaveButton = () => {
    if (isProcessing.current)
      return

    const path = currentFile.name
    const parentPath = path.substring(0, path.lastIndexOf('/'));
    const createdFile = new File([editorRef.current.getValue()], currentFile.name,
        { type: 'text/plain' });

    saveButtonRef.current.innerHTML = `<span class="loader small"></span>`
    isProcessing.current = true

    httpRequestFormData("/api/code/user-files/upload-file", {
      projectId: id,
      file: createdFile,
      directory: parentPath
    }).then(() => {
      saveButtonRef.current.textContent = "Сохранить"
      isProcessing.current = false
    })
  }

  const openGlobalContextMenu = (e, type) => {
    e.stopPropagation();
    setGlobalContextMenu(type)
  }

  return (
      <div className={styles.editorField}>
        <header>
          <div className={styles.name}>
            {currentFile?.name}
          </div>
          <div className={styles.projectActions}>
            <button style={{visibility: currentFile ? "visible" : "hidden"}} ref={saveButtonRef} id={"saveCode"}
                    onClick={handleSaveButton}>Сохранить</button>
            <button onClick={(e) => openGlobalContextMenu(e, "commit")}>Деплой</button>
            <button onClick={(e, ) => openGlobalContextMenu(e, "rollback")}>Откат</button>
          </div>

        </header>
        <div className={styles.editor} style={{visibility: currentFile && !globalContextMenu ? "visible" : "hidden"}}>
          <Editor width={"100%"}
                path={currentFile?.name}
                defaultValue={""} theme="vs-dark"
                onMount={editorOnMountEvent}
                language={languages[currentFile?.name.split(".").pop()]?.toLowerCase() || ""}
                options={{
                  fontFamily: "Consolas, 'Courier New', monospace",
                  fontSize: 17,
                  fontLigatures: true
                }}/>
        </div>

      </div>
    )
};

