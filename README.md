## Założenia

### Model

```
klocek{
	cena
	kształt
	fenotyp {
		//2(N)-1+1
		X (N), rotacja(N-1), w_plecaku(1)
	}
}

plecak
{
	rozmiar (N)
	kolekcja klocków //fenotyp
}
```

### Ewolucja

