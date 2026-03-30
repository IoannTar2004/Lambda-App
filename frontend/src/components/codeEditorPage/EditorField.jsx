import Editor from "@monaco-editor/react";
import {useContext, useEffect, useRef, useState} from "react";
import axios from "axios";
import styles from "../../css/CodeEditor.module.css";
import {FileContext} from "./CodeEditorPage.jsx";
import {languages} from "../../utils/languages.js";

export const EditorField = () => {

  const {currentContent, setCurrentContent} = useContext(FileContext)
  const [fileCache, setFileCache] = useState(new Map())
  const [currentFile, setCurrentFile] = useState("")
  const editorRef = useRef(null);

  useEffect(() => {
    if (!editorRef.current || !currentContent.name) return
    console.log(currentContent)

    const name = currentContent.name
    if (currentContent.upload)
      editorRef.current.setValue(currentContent.upload)
    else  {
      if (!fileCache.has(name)) {
        // запрос с сервера
        editorRef.current.setValue("print('hello')")
      }
    }

    setFileCache(prevState => {
        prevState.set(name, true)
        return prevState;
      });

  }, [currentContent.name]);

  const saveCode = () => {
    axios.post("/api/code/save-code",
        {
            filename: "script.py",
            code: editorRef.current.getValue(),
        }).then(() => console.log("ok")).catch(console.error)
  }


  const editorOnMountEvent = (e) => {
    editorRef.current = e
  }
  return (
      <div className={styles.editorField}>
        <header>
          {currentContent.name}
          <button>Сохранить</button>
        </header>
        <Editor width={"100%"}
                path={currentContent.name}
                defaultValue={""} theme="vs-dark"
                onMount={editorOnMountEvent}
                language={languages[currentContent.name.split(".").pop()] || ""}
                options={{
                  fontFamily: "Consolas, 'Courier New', monospace",
                  fontSize: 17,
                  fontLigatures: true
                }}
        />
      </div>
    )
};

