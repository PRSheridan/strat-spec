import { useState } from 'react'
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const block6Schema = z
  .object({
    example: z.string().optional(),
  })

type Block6Data = z.infer<typeof block6Schema>

interface GuitarBlock6Props {
  onNext: (data: Block6Data) => void
}

function GuitarBlock6({ onNext }: GuitarBlock6Props) {
  const { register, handleSubmit, watch, formState: { errors } } = useForm<Block6Data>({
    resolver: zodResolver(block6Schema),
    defaultValues: {
      example: "test",
    },
  })

  function onSubmit(data: Block6Data) {
  
    console.log("Block 4 Data:", data)
    onNext(data)
  }

  return (
    <div className="guitar-block">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h2>Block 4: Example</h2>

        <div className="guitar-block-section">
          <label>Example</label>
          <input
            type="number" step="any"
            {...register("example", { valueAsNumber: true })}
            placeholder="Enter a scale length (24–27 inches)"
          />
        </div>
        <button type="submit">Next</button>
      </form>
    </div>
  )
}

export default GuitarBlock6