import { useState, useEffect } from "react";

const API = import.meta.env.VITE_API_BASE;

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState(null);

  // cargar tareas
  async function fetchTasks() {
    try {
      setLoading(true);
      const res = await fetch(`${API}/tasks/`);
      if (!res.ok) throw new Error("Error cargando tareas");
      const data = await res.json();
      setTasks(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchTasks();
  }, []);

  // crear tarea
  async function addTask(e) {
    e.preventDefault();
    try {
      const res = await fetch(`${API}/tasks/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          description,
          completed: false,
        }),
      });
      if (!res.ok) throw new Error("Error creando tarea");
      const newTask = await res.json();
      setTasks([newTask, ...tasks]);
      setTitle("");
      setDescription("");
    } catch (e) {
      setError(e.message);
    }
  }

  // actualizar tarea (toggle completed)
  async function toggleTask(task) {
    try {
      const res = await fetch(`${API}/tasks/${task.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: task.title,
          description: task.description,
          completed: !task.completed,
        }),
      });
      if (!res.ok) throw new Error("Error actualizando tarea");
      const updated = await res.json();
      setTasks(tasks.map((t) => (t.id === updated.id ? updated : t)));
    } catch (e) {
      setError(e.message);
    }
  }

  // borrar tarea
  async function deleteTask(id) {
    try {
      const res = await fetch(`${API}/tasks/${id}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Error eliminando tarea");
      setTasks(tasks.filter((t) => t.id !== id));
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>To-Do List</h1>

      <form onSubmit={addTask} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Título"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: "10px", padding: "8px" }}
        />
        <textarea
          placeholder="Descripción"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{ display: "block", width: "100%", marginBottom: "10px", padding: "8px" }}
        />
        <button type="submit">Agregar tarea</button>
      </form>

      {error && <div style={{ color: "red", marginBottom: "10px" }}>{error}</div>}

      {loading ? (
        <p>Cargando...</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {tasks.map((task) => (
            <li
              key={task.id}
              style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "10px",
                marginBottom: "10px",
              }}
            >
              <h3 style={{ margin: "0 0 5px" }}>
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTask(task)}
                  style={{ marginRight: "8px" }}
                />
                {task.title}
              </h3>
              {task.description && <p>{task.description}</p>}
              <button onClick={() => deleteTask(task.id)} style={{ color: "red" }}>
                Eliminar
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
