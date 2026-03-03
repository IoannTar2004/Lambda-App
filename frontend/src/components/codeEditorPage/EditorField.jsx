import Editor from "@monaco-editor/react";
import {Fragment, useRef, useState} from "react";
import axios from "axios";

const EditorField = () => {

  const [file, setFile] = useState(true)
  const defaultCode = `def test():
    return True`

  const saveCode = () => {
    axios.post("/api/code/save-code",
        {
            filename: "script.py",
            code: editorRef.current.getValue(),
        }).then(() => console.log("ok")).catch(console.error)
  }

  const editorRef = useRef(null);

  const editorOnMountEvent = (e) => {
    editorRef.current = e
  }

  return (
      <Fragment>
        <button onClick={saveCode} id={"save-code"}>Сохранить</button>
        <Editor
          height="75%"
          width="99%"
          path={"script.py"}
          defaultValue={defaultCode}
          theme="vs-dark"
          onMount={editorOnMountEvent}
      />
      </Fragment>
  );
};

export default EditorField;