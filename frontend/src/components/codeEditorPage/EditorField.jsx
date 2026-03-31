import Editor from "@monaco-editor/react";
import {useContext, useEffect, useRef, useState} from "react";
import axios from "axios";
import styles from "../../css/CodeEditor.module.css";
import {FileContext} from "./CodeEditorPage.jsx";
import {languages} from "../../utils/languages.js";
import {HTTPMethods, httpRequest} from "../../utils/requests.js";
import {useParams} from "react-router";

export const EditorField = () => {

  const {id} = useParams()
  const {currentFile, setCurrentFile} = useContext(FileContext)
  const [fileCache, setFileCache] = useState(new Map())
  const editorRef = useRef(null);

  useEffect(() => {
    if (!editorRef.current || !currentFile) return

    const name = currentFile.name

    if (currentFile.upload)
      editorRef.current.setValue(currentFile.upload)

    else if (!fileCache.has(name)) {
      httpRequest(HTTPMethods.GET, "/api/code/user-files/download-file", {
        projectId: id,
        path: name
      }).then((e) => {
        setFileCache(prevState => {
          prevState.set(name, true)
          return prevState;
        });
        editorRef.current.setValue(e.data)
      })
    }

    setFileCache(prevState => {
      prevState.set(name, true)
      return prevState;
    });

  }, [currentFile]);

  const editorOnMountEvent = (e) => {
    editorRef.current = e
  }

  return (
      <div className={styles.editorField} style={{display: currentFile ? "block" : "none"}}>
        <header>
          {currentFile?.name}
          <button>Сохранить</button>
        </header>
        <Editor width={"100%"}
                path={currentFile?.name}
                defaultValue={""} theme="vs-dark"
                onMount={editorOnMountEvent}
                language={languages[currentFile?.name.split(".").pop()]?.toLowerCase() || ""}
                options={{
                  fontFamily: "Consolas, 'Courier New', monospace",
                  fontSize: 17,
                  fontLigatures: true
                }}
        />
      </div>
    )
};

