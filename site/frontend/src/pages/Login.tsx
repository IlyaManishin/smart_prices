import { useState } from "react"

export default function Login({ onSuccess }: { onSuccess: () => void }) {
    const [login, setLogin] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState(false)

    async function submit() {
        setError(false)
        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ login, password })
        })

        if (res.ok) onSuccess()
        else setError(true)
    }

    return (
        <div className="center">
            <h1>Умные ценники PVZ</h1>

            <input placeholder="Логин" value={login} onChange={e => setLogin(e.target.value)} />
            <input type="password" placeholder="Пароль" value={password} onChange={e => setPassword(e.target.value)} />

            <button onClick={submit}>Войти</button>

            {error && <div className="error">Неверный логин или пароль</div>}
        </div>
    )
}
