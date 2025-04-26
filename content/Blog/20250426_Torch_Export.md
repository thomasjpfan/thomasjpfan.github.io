Title: torch.export For Serializing Models and Faster Loading
Date: 2025-04-26 09:29
Tags: python, torch
Math: False
Metaimage: images/20250415_Torch_Export/meta.png

<!-- Metaimage code
from torch.export import export, save, load, Dim

batch_dim = Dim("batch", min=1, max=512)
exported_program = export(model, args=(X,), dynamic_shapes=({0: batch_dim}))

save(exported_program, "my_model.pt2")
loaded_model = load("my_model.pt2")
 -->

While `torch.compile` is great for *Just in time (JIT)* compilation, it adds significant startup time during prediction time. With PyTorch 2.6, `torch.export` can *Ahead of Time (AOT)* compile your PyTorch code and serialize it into a single zip file. When it works, `torch.export`'s AOT approach has faster startup times compared to `torch.compile`'s JIT. In this post, we learn about how to serialize and load a model using `torch.export`.

## Using `torch.export`

First, we load a ResNet152 `nn.Module` model onto a GPU and data that represents typical model input:

```python
from torchvision.models import resnet152

model = resnet152().to(torch.float32).cuda()
X = torch.randn(32, 3, 128, 128).to(torch.float32).cuda()
```

Next, we run `export` on the model and the input, while configuring a dynamic batch dimension:

```python
from torch.export import export, Dim

batch_dim = Dim("batch", min=1, max=512)
exported_program = export(model, args=(X,), dynamic_shapes=({0: batch_dim}))
```

Normally, `export` will AOT compile the model to only work with the exact shape of the input. By setting `dynamic_shape=({0: batch_dim})`, we configure the compiler to allow the 0th indexed batch dimension to be a value between 1 and 512.

With the `exported_program`, we can run the model through a forward pass by calling `.module()` to extract the module:

```python
exported_module = exported_program.module()
X_out = exported_module(X)
```

Finally, we can save the exported model by calling `save` with a file path:

```python
from torch.export import save

save(exported_program, "resnet152.pt2")
```

## Loading the model

With a serialized model, we can now run `torch.export.load` to load the model and run a forward pass with the data:

```python
from torch.export import load

model = timed(load, "resnet152.pt2")
# Duration: 1.2s

result = timed(model.module(), X)
# Duration: 0.2s
```

The model takes **1.2s** to load and **0.2s** to use the loaded model to do a forward pass. For comparison, we can compile the same model with `torch.compile`'s JIT:

```python
model_opt = torch.compile(model, mode="reduce-overhead", fullgraph=True)
timed(model_opt, X)
# Duration: 21.1s
```

The first run takes **21.1s**, because `torch.compile` is compiling from scratch. When we run it again with a warm cache, it takes **8.9s**. Comparing the total time for initially loading the model and running a prediction, we get these total runtimes:


| `torch.export` | `torch.compile`: warm cache | `torch.compile`: cold cache |
| -------------: | --------------------------: | --------------------------: |
|           1.4s |                        8.9s |                       21.1s |

Using `torch.export`'s AOT has faster startup times compared to `torch.compile`'s JIT!

## Conclusion

Although `torch.export` is faster compared to `torch.compile`, `export` has one **big tradeoff**:

- `torch.export` requires full graph capture, which is **more restrictive**. `torch.compile` has the option to fall back to a Python interpreter for untraceable code, enabling `compile` to run any arbitrary Python code.

If you can capture the full graph, then `torch.export` has two **major benefits**:

- You can load the serialized model from a non-Python environment such as **C++**. To learn more about this feature see the [AOTInductor documentation for torch.export](https://pytorch.org/docs/main/torch.compiler_aot_inductor.html).
- As shown in this post, the **startup times are faster**.

Overall, I find it remarkable that we have the choice between using AOT and JIT for running our PyTorch code, each with its own tradeoffs. You can learn more in [torch.export's documentation](https://pytorch.org/docs/stable/export.html).
