import { HomePage } from './pages/HomePage'
import './App.css'

/**
 * 根组件：Round 0 仅挂载首页（上传 + 文案 + 模板 + 任务状态占位）。
 */
function App() {
  return (
    <div className="app-root">
      <HomePage />
    </div>
  )
}

export default App
