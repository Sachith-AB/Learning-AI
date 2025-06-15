import {BrowserRouter, Route, Routes} from 'react-router-dom';
import Search from './pages/Search';
import ChatPage from './pages/ChatPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Search/>}/>
        <Route path='/chat' element={<ChatPage/>}/>
      </Routes>
    </BrowserRouter>
  )
}
