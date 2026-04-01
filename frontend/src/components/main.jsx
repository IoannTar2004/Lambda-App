import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '../css/index.css'
import {BrowserRouter, Route, Routes} from "react-router";
import {VkCloudTemplate} from "./vkCloud/VkCloudTemplate.jsx";
import {StartPage} from "./start/StartPage.jsx";
import {FunctionsListPage} from "./functions/FunctionsListPage.jsx";
import {FunctionPage} from "./functions/FunctionPage.jsx";
import {EditPage} from "./functions/EditPage.jsx";
import {DeletePage} from "./functions/DeletePage.jsx";
import {LogsPage} from "./logs/LogsPage.jsx";
import {CodeEditorPage} from "./codeEditorPage/CodeEditorPage.jsx";
import {CreateProjectPage} from "./start/CreateProjectPage.jsx";
import {CreateFunctionPage} from "./functions/CreateFunctionPage.jsx";

const baseURL = "/app/project123456/services/lambda"

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path={baseURL} element={<VkCloudTemplate />}>
          <Route path={"start"} element={<StartPage />}></Route>
          <Route path={"start/create-project"} element={<CreateProjectPage />}></Route>
          <Route path={"functions"} element={<FunctionsListPage />}></Route>
          <Route path={"functions/:id"} element={<FunctionPage />}></Route>
          <Route path={"functions/create"} element={<CreateFunctionPage />}></Route>
          <Route path={"functions/:id/edit"} element={<EditPage />}></Route>
          <Route path={"functions/:id/delete"} element={<DeletePage />}></Route>
          <Route path={"functions/:id/logs/:log_id"} element={<LogsPage />}></Route>
          <Route path={"projects/:id"} element={<CodeEditorPage />}></Route>
        </Route>
      </Routes>
    </BrowserRouter>

  </StrictMode>
)
