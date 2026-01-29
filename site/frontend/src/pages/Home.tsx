import { useEffect, useState } from "react"

type Board = {
    id: number
    product: string
    base_price: number
    discount: number
    installed_at: string
    synced: boolean
}

export default function Home() {
    const [boards, setBoards] = useState<Board[]>([])
    const [edited, setEdited] = useState(false)

    useEffect(() => {
        fetch("/api/boards")
            .then(r => r.json())
            .then(setBoards)
    }, [])

    function updateBoard(index: number, field: keyof Board, value: any) {
        setBoards(prev => {
            const copy = [...prev]
            copy[index] = { ...copy[index], [field]: value, synced: false }
            return copy
        })
        setEdited(true)
    }

    function applyChanges() {
        setEdited(false)
    }

    return (
        <div className="page">
            <h1 className="page-title">Умные ценники</h1>

            <div className="table-card">
                <table>
                    <thead>
                        <tr>
                            <th>№</th>
                            <th>Товар</th>
                            <th>Цена</th>
                            <th>Скидка %</th>
                            <th>Дата установки</th>
                            <th>Статус</th>
                            <th></th>
                        </tr>
                    </thead>

                    <tbody>
                        {boards.map((b, i) => (
                            <tr key={b.id}>
                                <td>{b.id}</td>

                                <td>
                                    <div className="product">{b.product}</div>
                                </td>

                                <td>
                                    <input
                                        className="table-input"
                                        type="number"
                                        value={b.base_price}
                                        onChange={e => updateBoard(i, "base_price", +e.target.value)}
                                    />
                                </td>

                                <td>
                                    <input
                                        className="table-input"
                                        type="number"
                                        value={b.discount}
                                        onChange={e => updateBoard(i, "discount", +e.target.value)}
                                    />
                                </td>

                                <td>
                                    <input
                                        className="table-input"
                                        type="date"
                                        value={b.installed_at}
                                        onChange={e => updateBoard(i, "installed_at", e.target.value)}
                                    />
                                </td>

                                <td className={b.synced ? "sync-ok" : "sync-wait"}>
                                    {b.synced ? "Обновлено" : "Ожидание"}
                                </td>

                                <td>
                                    <button
                                        className={
                                            "apply-btn " + (edited ? "active" : "disabled")
                                        }
                                        disabled={!edited}
                                        onClick={applyChanges}
                                    >
                                        Принять
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
