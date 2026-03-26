import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '../css/index.css'
import {BrowserRouter, Route, Routes} from "react-router";
import {VkCloudTemplate} from "./vkCloud/VkCloudTemplate.jsx";
import {StartPage} from "./app/StartPage.jsx";

const baseURL = "/app/project123456/services/lambda"

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path={baseURL} element={<VkCloudTemplate />}>
          <Route path={"start"} element={<StartPage />}></Route>
        </Route>
      </Routes>
    </BrowserRouter>

  </StrictMode>
)
