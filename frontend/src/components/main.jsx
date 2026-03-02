import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '../css/index.css'
import {CodeEditorPage} from "./codeEditorPage/CodeEditorPage.jsx";

createRoot(document.getElementById('root')).render(
  <StrictMode>
      <CodeEditorPage />
  </StrictMode>
)
