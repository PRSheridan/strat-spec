import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

// Validation Schema
const block2Schema = z
  .object({
    name: z.string().min(3, "Guitar name must be at least 3 characters"),
    modified: z.boolean(),
    modifications: z.string().optional(),
    description: z.string().optional(),
    images: z.array(z.instanceof(File)).optional(),
  })
  .refine((data) => {
    // If modified is true, modifications must not be empty
    if (data.modified && (!data.modifications || data.modifications.trim().length === 0)) {
      return false
    }
    return true
  }, {
    message: "Please describe the modifications",
    path: ["modifications"],
  })


type Block2Data = z.infer<typeof block2Schema>

interface GuitarBlock2Props {
  onNext: (data: Block2Data) => void
}

function GuitarBlock2({ onNext }: GuitarBlock2Props) {
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm<Block2Data>({
    resolver: zodResolver(block2Schema),
    defaultValues: {
      name: "",
      modified: false,
      modifications: "",
      description: "",
      images: [],
    },
  })

  const modified = watch("modified")

  const onSubmit = (data: Block2Data) => {
    console.log("Block 2 Data:", data)
    onNext(data)
  }

  return (
    <div className="guitar-block">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h2>Block 2: Personalization</h2>

        <div>
          <label>Guitar Name</label>
          <input {...register("name")} placeholder="Enter guitar name" />
          {errors.name && <p>{errors.name.message}</p>}
        </div>

        <div>
          <label>Modified?</label>
          <input type="checkbox" {...register("modified")} />
        </div>

        {modified && (
          <div>
            <label>Modifications</label>
            <input {...register("modifications")} placeholder="Describe modifications" />
            {errors.modifications && <p>{errors.modifications.message}</p>}
          </div>
        )}

        <div>
          <label>Description (Optional)</label>
          <textarea {...register("description")} placeholder="Enter guitar description" />
        </div>

        <div>
          <label>Upload Images</label>
          <input type="file" multiple onChange={(e) => {
            setValue("images", Array.from(e.target.files || []))
          }} />
        </div>

        <button type="submit">Next</button>
      </form>
    </div>
  )
}

export default GuitarBlock2
