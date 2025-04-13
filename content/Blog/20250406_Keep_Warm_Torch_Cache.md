Title: Keep Warm with Portable torch.compile Caches
Date: 2025-04-06 09:29
Tags: python, torch
Math: False
Metaimage: images/20250406_Keep_Warm_Torch_Cache/meta.png

PyTorch's `compile` function improves performance of your code by compiling and caching the computational graph for later use. `torch.compile` has a notion of a "cold compile" and a "warm compile", where "cold" is the first run and "warm" is faster by using a cache. The latest torch nightly wheel introduces a portable caching solution loadable on separate machines. In this post, we learn about this new caching solution and how it keeps your cache warm!

## Cold vs Warm Compile Runtimes

In this example, we run `torch.compile` on a ResNet152 `nn.Module` without a cache and measure the cold start run:

```python
from torchvision.models import resnet152

model = resnet152().to(torch.float32).cuda()
model_opt = torch.compile(model, mode="reduce-overhead", fullgraph=True)
X = torch.randn(32, 3, 128, 128).to(torch.float32).cuda()

timed(model_opt, X)
# Duration: 21.1s
```

The first run takes **21.1s**, because `torch.compile` is compiling from scratch. When we run again, the cache is warm
and the duration goes down to **8.9s** which is 2x faster than a cold start!

## Portable Cache

What if we wanted to populate the cache once on one machine and use that to warm up the cache for many machines? I have found success by adjusting the cache directory using `TORCHINDUCTOR_CACHE_DIR`, saving the entire directory, and loading the directory on the new machine. With the latest torch nightly, there is a new option: `torch.compiler.save_cache_artifacts` and `torch.compiler.load_cache_artifacts`.

With `torch.compiler.save_cache_artifacts`, we have a Python API for saving the cache as a binary file. In this example, we save the artifact as "artifact.bin":

```python
artifact_path = Path("artifact.bin")

artifact_bytes, _ = torch.compiler.save_cache_artifacts()
save_artifact_path.write_bytes(artifact_bytes)
```

On a separate machine, we load the "artifact.bin" which warms up the cache!

```python
artifact_bytes = artifact_path.read_bytes()
torch.compiler.load_cache_artifacts(artifact_bytes)
```

To learn more, refer to the [documentation](https://pytorch.org/tutorials/recipes/torch_compile_caching_tutorial.html#torch-compile-end-to-end-caching-mega-cache) for `save_cache_artifacts` and `load_cache_artifacts`.

## Conclusion

Now that frameworks, such as SGLang and vLLM, use `torch.compile` to speed up workloads, it is also important to optimize for startup times so we can scale up faster to meet demand. Keeping the torch cache warm is one dimension where we can improve startup times. The new `{save,load}_cache_artifact` API gives us a more portable way to keep the cache warm on multiple machines.
