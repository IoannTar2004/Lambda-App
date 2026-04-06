import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '../css/index.css'
import {BrowserRouter, Route, Routes} from "react-router";
import {VkCloudTemplate} from "./vkCloud/VkCloudTemplate.jsx";
import {StartPage} from "./start/StartPage.jsx";
import {FunctionsListPage} from "./functions/FunctionsListPage.jsx";
import {FunctionPage} from "./functions/FunctionPage.jsx";
import {EditFunctionPage} from "./functions/EditFunctionPage.jsx";
import {DeleteFunctionPage} from "./functions/DeleteFunctionPage.jsx";
import {LogsPage} from "./logsPage/LogsPage.jsx";
import {CodeEditorPage} from "./codeEditorPage/CodeEditorPage.jsx";
import {CreateProjectPage} from "./start/CreateProjectPage.jsx";
import {CreateFunctionPage} from "./functions/CreateFunctionPage.jsx";
import {DeleteProjectPage} from "./start/DeleteProjectPage.jsx";

const baseURL = "/app/project123456/services/lambda"

createRoot(document.getElementById('root')).render(
  // <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path={baseURL} element={<VkCloudTemplate />}>
          <Route path={"start"} element={<StartPage />}></Route>
          <Route path={"start/create-project"} element={<CreateProjectPage />}></Route>
          <Route path={"projects/:projectId/delete"} element={<DeleteProjectPage />}></Route>
          <Route path={"projects/:projectId/functions"} element={<FunctionsListPage />}></Route>
          <Route path={"projects/:projectId/functions/:id"} element={<FunctionPage />}></Route>
          <Route path={"projects/:projectId/functions/create"} element={<CreateFunctionPage />}></Route>
          <Route path={"projects/:projectId/functions/:id/edit"} element={<EditFunctionPage />}></Route>
          <Route path={"projects/:projectId/functions/:id/delete"} element={<DeleteFunctionPage />}></Route>
          <Route path={"projects/:projectId/functions/:id/logs/:run_id"} element={<LogsPage />}></Route>
          <Route path={"projects/:id/editor"} element={<CodeEditorPage />}></Route>
        </Route>
      </Routes>
    </BrowserRouter>

  // </StrictMode>
)
