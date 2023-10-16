import './Input.css';
import Header from '../header/Header'
import Nav from '../nav/Nav';

function Input() {
  return (
    <div className='input-div'>
      <Header /> 
      <Nav />
      <h1 className='input-title'>Book</h1>
      <h2 className='input-directions'>Enter a book title and author</h2>
      <div className='input-section'>
        <p className='input-category'>Title:</p>
        <input type="text" />
      </div>
      <div className='input-section'>
        <p className='input-category'>Author:</p>
        <input type="text" />
      </div>
      <div className='input-button-div'>
        <button className='input-button'>Submit</button>
      </div>
    </div>
  )
}
export default Input