import RegisterStudent from "./pages/RegisterStudent";
import RegisterTeacher from "./pages/RegisterTeacher";
import CreateClass from "./pages/CreateClass";
import Recognize from "./pages/Recognize";
import AssignTeacher from "./pages/AssignTeacher";
import AssignStudents from "./pages/AssignStudents";
import GetReport from "./pages/GetReport"; // ✅ ADD THIS

function App() {
  return (
    <div>
      <h1>Face Attendance System</h1>

      <RegisterStudent />
      <RegisterTeacher />
      <CreateClass />
      <Recognize />
      <AssignTeacher />
      <AssignStudents />

      <GetReport /> {/* ✅ ADD THIS */}
    </div>
  );
}

export default App;