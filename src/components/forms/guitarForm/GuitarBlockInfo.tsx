

function GuitarBlockInfo({ onNext }: any) {
  return (
    <div className="guitar-block">
      <h2>Guitar Build Information</h2>
      <div className="guitar-block-section">
        <label>Page with information about adding a guitar to your profile.</label>
        <p>* indicates a field is required</p>
      </div>
      <button onClick={() => onNext({})}>Next</button>
    </div>
  )
}

export default GuitarBlockInfo