import { useState } from "react";
import styles from "./main.module.css";
import { Link } from "react-router-dom";

function Calendar({}) {
    return (
        <div>
            <div className={styles.container}>
                <div className={styles.flex}></div>
                <div className={styles.nav_container}>
                    <span className={styles.title}>2023년 7월</span>
                    <button className={styles.button}><Link to={`/plan`}>＜</Link></button>
                    <button className={styles.button}><Link to={`/todo`}>＞</Link></button>
                    <button className={styles.add_button}>＋</button>
                </div>
                <div className={styles.days_container}>
                    <span className={styles.days}>일</span>
                    <span className={styles.days}>월</span>
                    <span className={styles.days}>화</span>
                    <span className={styles.days}>수</span>
                    <span className={styles.days}>목</span>
                    <span className={styles.days}>금</span>
                    <span className={styles.days}>토</span>
                </div>
                <div className={styles.daysNum_container}><button className={styles.daysNum}>22</button>
                    <button className={styles.daysNum}>23</button>
                    <button className={styles.daysNum}>24</button>
                    <button className={styles.daysNum}>25</button>
                    <button className={styles.daysNum}>26</button>
                    <button className={styles.daysNum}>27</button>
                    <button className={styles.daysNum}>28</button></div>
                    <div className={styles.goal_container}>

                    </div>
                <div className={styles.event_container}>
                    <div className={styles.nav_container2}>
                        <button className={styles.nobackbutton}>일정</button>
                        <button className={styles.nobackbutton}>할 일</button>
                        <button></button>
                    </div>
                    
                </div></div>

        </div>
    )

}

export default Calendar;